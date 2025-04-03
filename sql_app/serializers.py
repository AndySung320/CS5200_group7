from rest_framework import serializers
from .models import SQLProblem, Topic, Hint, Attempt
from users.models import User
from django.conf import settings
import os, glob, json
from utils.sql_sandbox import run_problem_setup, get_solution_output, sandbox_schema, check_user_query
from config.db_config import get_mysql_db_config
import traceback

class SQLProblemListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing basic SQL problem information.

    This serializer is used to present a simplified view of SQLProblem objects,
    typically in list views or overview pages.

    Features:
    - Includes the problem's ID, title, difficulty level, topic name, and acceptance rate.
    - The topic field is derived from the related Topic model's `name` attribute.
    - The acceptance field represents the percentage of correct submissions (0.0 - 100.0).

    Fields:
        problem_id (int): Unique identifier for the problem.
        title (str): Title of the problem.
        difficulty_level (str): Difficulty level ('Easy', 'Medium', etc.).
        topic (str): Name of the related topic (e.g., 'JOIN', 'GROUP BY').
        acceptance (float): Percentage of successful attempts, rounded to 2 decimal places.

    Example Output:
        {
            "problem_id": 1,
            "title": "Find the Top Seller",
            "difficulty_level": "Medium",
            "topic": "Aggregation",
            "acceptance": 83.33
        }
    """
    topic = serializers.CharField(source='topic.name')  ## Gets topic name from the related Topic model
    acceptance = serializers.FloatField()
    class Meta:
        model = SQLProblem
        fields = ['problem_id', 'title', 'difficulty_level', 'topic', 'acceptance']

class TableColumnSerializer(serializers.Serializer):
    """
    Serializer for representing metadata about a table column.

    This serializer is typically used to describe the structure of a database table,
    including the column's name, data type, and an optional description.

    Fields:
        name (str): The name of the column (e.g., 'employee_id').
        type (str): The SQL data type of the column (e.g., 'INT', 'VARCHAR(255)').
        description (str, optional): A human-readable explanation of the column's purpose.

    Example Input/Output:
        {
            "name": "employee_id",
            "type": "INT",
            "description": "Primary key for the employee table"
        }

    Notes:
    - The `description` field is optional and can be omitted in input/output.
    - This serializer is not tied to any model; it’s used for custom, schema-like data structures.
    """
    name = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField(required=False)

class TableSchemaSerializer(serializers.Serializer):
    """
    Serializer for representing the schema of a database table.

    This serializer is used to describe a table's structure, including its name
    and a list of its columns (each described by TableColumnSerializer).

    Fields:
        table_name (str): The name of the table (e.g., 'Employees').
        columns (List[TableColumnSerializer]): A list of column definitions, where each column includes:
            - name: Column name (e.g., 'employee_id')
            - type: SQL type (e.g., 'INT', 'VARCHAR(255)')
            - description (optional): Explanation of the column's purpose

    Example Output:
        {
            "table_name": "Employees",
            "columns": [
                {
                    "name": "employee_id",
                    "type": "INT",
                    "description": "Primary key"
                },
                {
                    "name": "name",
                    "type": "VARCHAR(100)",
                    "description": "Employee's full name"
                }
            ]
        }

    Notes:
    - This serializer is useful for APIs that preview table schemas before executing SQL queries.
    - It is not tied to a database model and can be used for custom schema definitions.
    """
    table_name = serializers.CharField()
    columns = TableColumnSerializer(many=True)

class SQLProblemDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for providing detailed information about a single SQL problem.

    This serializer includes:
    - Basic metadata (title, description, difficulty, topic)
    - Hints associated with the problem
    - Input table schemas (loaded from metadata.json)
    - Whether the result requires row order preservation
    - The expected query output (executed in a sandbox)

    Fields:
        problem_id (int): Unique ID of the SQL problem.
        title (str): Title of the problem.
        description (str): Problem statement and requirements.
        difficulty_level (str): One of 'Easy', 'Medium', 'Hard', 'Expert'.
        topic (str): The name of the associated topic (e.g., 'JOIN').
        requires_order (bool): Whether the output rows must be in a specific order.
        tables (List[dict]): List of table schema objects, loaded from metadata.json.
        hints (List[str]): Ordered list of hint texts associated with the problem.
        expected_output (List[dict] or dict): The correct query output for this problem.
                                              If execution fails, returns an error object.

    Notes:
    - Table schema and order requirement are loaded from a `metadata.json` file in the problem's folder.
    - The expected output is dynamically generated by running the provided DDL and solution SQL in a temporary schema.
    - All helper methods handle exceptions gracefully.

    Example Output:
        {
            "problem_id": 3,
            "title": "Find Active Users",
            "description": "...",
            "difficulty_level": "Medium",
            "topic": "JOIN",
            "requires_order": false,
            "tables": [...],
            "input_data": [...],
            "hints": ["Try filtering by login count", "Use GROUP BY"],
            "expected_output": [...]
        }
    """
    topic = serializers.CharField(source='topic.name')
    hints = serializers.SerializerMethodField()
    tables = serializers.SerializerMethodField()
    input_data = serializers.SerializerMethodField()
    expected_output = serializers.SerializerMethodField()
    requires_order = serializers.SerializerMethodField()
    acceptance = serializers.SerializerMethodField()

    class Meta:
        model = SQLProblem
        fields = [
            'problem_id', 'title', 'description', 'difficulty_level',
            'topic', 'requires_order', 'tables', 'input_data', 'hints', 'expected_output', 'acceptance'
        ]

    def get_hints(self, obj):
        # Retrieve hint texts ordered by hint_order
        return list(Hint.objects.filter(problem_id=obj.problem_id).order_by('hint_order').values_list('hint_text', flat=True))

    def get_tables(self, obj):
        # Load table schema definitions from metadata.json
        base_path = os.path.join(settings.BASE_DIR, "problems")
        pattern = os.path.join(base_path, str(obj.problem_id).zfill(3), "metadata.json")
        for meta_file in glob.glob(pattern):
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f).get("tables", [])
        return []

    def get_requires_order(self, obj):
        # Check whether the problem requires row order in output
        base_path = os.path.join(settings.BASE_DIR, "problems")
        pattern = os.path.join(base_path, str(obj.problem_id).zfill(3), "metadata.json")
        for meta_file in glob.glob(pattern):
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f).get("requires_order", False)
        return False

    def get_expected_output(self, obj):
        # Load expected_output from metadata.json
        try:
            base_path = os.path.join(settings.BASE_DIR, "problems")
            pattern = os.path.join(base_path, str(obj.problem_id).zfill(3), "metadata.json")
            for meta_file in glob.glob(pattern):
                with open(meta_file, "r", encoding="utf-8") as f:
                    return json.load(f).get("expected_output", [])
        except Exception:
            return {"error": traceback.format_exc()}
        
    def get_acceptance(self, obj):
        from sql_app.models import Attempt
        total = Attempt.objects.filter(problem=obj).count()
        correct = Attempt.objects.filter(problem=obj, status="Completed").count()
        if total == 0:
            return 0.0
        return round(correct / total * 100, 2)
    
    def get_input_data(self, obj):
        # Load input_data from metadata.json
        base_path = os.path.join(settings.BASE_DIR, "problems")
        pattern = os.path.join(base_path, str(obj.problem_id).zfill(3), "metadata.json")
        for meta_file in glob.glob(pattern):
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f).get("input_data", [])
        return

class AttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for submitting and recording a user's attempt at solving a SQL problem.

    Features:
    - Accepts a user-submitted SQL query via the `user_query` field (write-only).
    - Uses `check_user_query()` to validate the SQL logic and compute correctness.
    - Automatically calculates score and status based on validation result.
    - Saves the attempt data to the database.
    - Stores additional feedback (e.g., diff message) in `self.context['check_result']`.

    Fields:
        attempt_id (int, read-only): Auto-generated primary key.
        user (User): The user who submitted the attempt.
        problem (SQLProblem): The problem being solved.
        submission_date (datetime, read-only): Timestamp when the attempt is created.
        score (decimal, read-only): 100.0 if correct, 0.0 otherwise.
        status (str, read-only): 'Completed' or 'Failed', depending on correctness.
        time_taken (int, optional): Time spent on the problem (in seconds).
        hints_used (int): Number of hints used by the user.
        user_query (str, write-only): SQL query submitted by the user; used for checking but not stored.

    Example Input:
        {
            "user": 1,
            "problem": 3,
            "time_taken": 120,
            "hints_used": 1,
            "user_query": "SELECT * FROM Employees WHERE salary > 50000"
        }

    Example Output:
        {
            "attempt_id": 42,
            "user": 1,
            "problem": 3,
            "submission_date": "2025-03-30T15:45:00Z",
            "score": 100.0,
            "status": "Completed",
            "time_taken": 120,
            "hints_used": 1
        }

    Notes:
    - `user_query` is not saved to the database.
    - Any feedback from the SQL checker is stored in `self.context['check_result']` (accessible after save).
    """
    user_query = serializers.CharField(write_only=True)  # Used for checking, not stored in DB

    class Meta:
        model = Attempt
        fields = ['attempt_id', 'user', 'problem', 'submission_date', 'score', 'time_taken', 'status', 'hints_used', 'user_query']
        read_only_fields = ['attempt_id', 'submission_date', 'score', 'status']  # Auto-set by backend

    def create(self, validated_data):
        user = validated_data['user']
        problem = validated_data['problem']
        user_query = validated_data.pop('user_query')
        hints_used = validated_data.get('hints_used', 0)
        time_taken = validated_data.get('time_taken', None)

        is_correct, message = check_user_query(problem.problem_id, user_query)

        # Check the user's query and determine result
        score = 100.0 if is_correct else 0.0
        status = 'Completed' if is_correct else 'Failed'

        # Create and save the Attempt record
        attempt = Attempt.objects.create(
            user=user,
            problem=problem,
            score=score,
            status=status,
            hints_used=hints_used,
            time_taken=time_taken,
        )

        # Store the check result (e.g., diff message) in serializer context
        self.context['check_result'] = message
        return attempt

class AttemptHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for representing a user's attempt history on a specific problem.

    This serializer is used to return a summary of past attempts, including:
    - When the user submitted their answer
    - Their score
    - How much time they spent
    - The result status (e.g., Completed, Failed)
    - How many hints were used

    Fields:
        - submission_date (datetime): Timestamp of when the attempt was submitted.
        - score (decimal): The score the user received for the attempt.
        - time_taken (int): Time spent on the attempt, in seconds.
        - status (str): Status of the attempt ('Completed', 'In Progress', etc.).
        - hints_used (int): Number of hints used during the attempt.
    """
    class Meta:
        model = Attempt
        fields = ['submission_date', 'score', 'time_taken', 'status', 'hints_used']