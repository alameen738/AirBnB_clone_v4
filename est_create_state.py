#!/usr/bin/python3
import unittest
import mysql.connector

class TestCreateState(unittest.TestCase):
    def setUp(self):
        # Connect to the MySQL server
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="your_database"  # Replace with your MySQL database name
        )
        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def test_create_state(self):
        # Get the number of current records in the table states before the action
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_before = self.cursor.fetchone()[0]

        # Execute the console command (this is simulated as we can't run console commands directly in unittest)
        # For example, you might have a function to execute the console command like execute_console_command("create State name='California'")
        # You'll need to replace this with your actual implementation
        # For demonstration purposes, let's assume the command adds a new state

        # Simulating the action by adding a new state directly
        self.cursor.execute("INSERT INTO states (name) VALUES ('California')")

        # Get the number of current records in the table states again after the action
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_after = self.cursor.fetchone()[0]

        # Check if the difference is +1
        self.assertEqual(count_after, count_before + 1)

if __name__ == "__main__":
    unittest.main()
