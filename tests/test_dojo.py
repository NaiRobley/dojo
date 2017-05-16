import os
import sys
import unittest
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.person import Fellow, Staff
from system.room import Office, LivingSpace
from system.dojo import Dojo


class DojoTestCases(unittest.TestCase):
    """
    Tests for the Dojo class
    """
    def setUp(self):
        self.new_dojo = Dojo()
        self.new_dojo.create_room("Blue", "office")
        self.new_dojo.create_room("Mara", "livingspace")
        self.new_dojo.add_person("Another", "Lady", "fellow", True)

    def test_create_room(self):
        """
        Test the creation of a new office and livingspace
        """
        initial_office_count = len(self.new_dojo.rooms['offices'])
        office_yellow = self.new_dojo.create_room("Yellow", "office")
        self.assertIn(office_yellow, self.new_dojo.rooms['offices'])
        new_office_count = len(self.new_dojo.rooms['offices'])
        self.assertEqual(new_office_count - initial_office_count, 1)

        initial_livingspace_count = len(self.new_dojo.rooms["livingspaces"])
        livingspace_tsavo = self.new_dojo.create_room("Tsavo", "livingspace")
        self.assertIn(livingspace_tsavo, self.new_dojo.rooms["livingspaces"])
        new_livingspace_count = len(self.new_dojo.rooms["livingspaces"])
        self.assertEqual(new_livingspace_count - initial_livingspace_count, 1)

    def test_add_person(self):
        """
        Test the creation of a new fellow and staff
        """
        initial_fellow_count = len(self.new_dojo.people['fellows'])
        new_fellow = self.new_dojo.add_person("Robley", "Gori", "fellow", True)
        self.assertIn(new_fellow, self.new_dojo.people["fellows"])
        new_fellow_count = len(self.new_dojo.people['fellows'])
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

        initial_staff_count = len(self.new_dojo.people['staff'])
        new_staff = self.new_dojo.add_person("Faith", "Gori", "staff")
        self.assertIn(new_staff, self.new_dojo.people["staff"])
        new_staff_count = len(self.new_dojo.people['staff'])
        self.assertEqual(new_staff_count - initial_staff_count, 1)

    def test_print_allocations(self):
        """
        Test that allocations are printed on the screen
        and also output to file
        """
        # Data is entered
        self.new_dojo.add_person("Faith", "Gori", "staff")
        self.new_dojo.add_person("Robley", "Gori", "fellow", True)
        self.new_dojo.print_allocations("newfile.txt")
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "newfile.txt")
        # Check if file is created
        self.assertTrue(os.path.exists(file))

        with open(file) as myfile:
            lines = myfile.readlines()
            self.assertIn("Blue - office\n", lines)
            self.assertIn("Mara - livingspace\n", lines)
            self.assertIn("Faith Gori\n", lines)
            self.assertIn("Robley Gori\n", lines)
        os.remove(file)

    def test_load_people(self):
        """
        Test that people can be loaded from a text file and created
        The dictionary of people is supposed to be updated to include the new additions
        """
        self.new_dojo.load_people("test_load_people_file.txt")
        # People from file are added to application
        total_people = len(self.new_dojo.people['fellows']) + len(self.new_dojo.people['staff'])
        self.assertEqual(8, total_people)
        self.assertEqual(5, len(self.new_dojo.people['fellows']))
        self.assertEqual(3, len(self.new_dojo.people['staff']))

    def test_print_room(self):
        """
        Test that you can print the room members in a certain room.
        The function is supposed to return the allocations as a string.
        Also check if the room members appear in the list
        """
        self.new_dojo.add_person("Faith", "Gori", "staff")
        self.new_dojo.add_person("Robley", "Gori", "fellow", True)
        self.assertTrue(isinstance(self.new_dojo.print_room("Mara"), str))
        self.assertIn("Blue - office\n", self.new_dojo.print_room("Blue"))
        self.assertIn("Mara - livingspace\n", self.new_dojo.print_room("Mara"))
        self.assertIn("Faith Gori\n", self.new_dojo.print_room("Blue"))
        self.assertIn("Robley Gori\n", self.new_dojo.print_room("Mara"))

    def test_get_person_id(self):
        """
        Test that a user can get the id of a person or people with common names to use to reallocate them
        A list of the people matching the name is returned
        """
        # create the person
        self.new_dojo.add_person("Robley", "Gori", "staff")
        person_id = self.new_dojo.get_person_id("Robley Gori")
        self.assertTrue(isinstance(person_id, list))

    def test_get_person_object(self):
        """
        Test that you can find a user by their id and return them as an object for reallocation
        """
        # Add the person
        self.new_dojo.add_person("New", "Person", "fellow", True)
        self.new_dojo.add_person("New", "Lady", "staff")

        # Get their id
        new_staff = self.new_dojo.get_person_id("New Lady")[0]
        new_fellow = self.new_dojo.get_person_id("New Person")[0]

        # Use their id to get their object
        staff = self.new_dojo.get_person_object(new_staff.p_id)
        fellow = self.new_dojo.get_person_object(new_fellow.p_id)

        # Assert if the objects are instances of their respective classes
        self.assertTrue(isinstance(fellow, Fellow))
        self.assertTrue(isinstance(staff, Staff))

    def test_check_room(self):
        """
        Test that you can check if the room that the person is to be reallocated to exists
        and is available
        """
        self.new_dojo.create_room("Teal", "office")
        self.new_dojo.create_room("Kenya", "livingspace")
        office = self.new_dojo.check_room("Teal", "Robley Gori")
        livingspace = self.new_dojo.check_room("Kenya", "Robley Gori")
        no_office = self.new_dojo.check_room("Another", "Robley Gori")
        self.assertTrue(isinstance(office, Office))
        self.assertTrue(isinstance(livingspace, LivingSpace))
        self.assertFalse(no_office)

    def test_get_old_office(self):
        """
        Test that you can get a person old office before reallocating them to a new one
        """
        old_office = self.new_dojo.get_old_office("Another Lady")
        no_old_office = self.new_dojo.get_old_office("No Guy")
        self.assertTrue(isinstance(old_office, Office))
        self.assertFalse(no_old_office)

    def test_get_old_livingspace(self):
        """
        Test that you can get a person old living space before reallocating them to a new one
        """
        old_livingspace = self.new_dojo.get_old_livingspace("Another Lady")
        no_old_livingspace = self.new_dojo.get_old_livingspace("No Guy")
        self.assertTrue(isinstance(old_livingspace, LivingSpace))
        self.assertFalse(no_old_livingspace)

    def test_reallocate(self):
        """
        Test that you can reallocate a person to a new room
        """
        # create the person
        new_person = self.new_dojo.add_person("Robley", "Gori", "staff")
        # create a new empty room
        new_office = self.new_dojo.create_room("Yellow", "office")

        # check current room of the person
        for office in self.new_dojo.rooms['offices']:
            # Get the room in which the person is in
            if new_person in office.r_occupants:
                old_office = office

        # reallocate the person to new office
        self.new_dojo.reallocate_person(new_person.p_id, new_office.r_name)

        # Check if reallocation was successful
        new_office_location = self.new_dojo.rooms['offices'].index(new_office)
        new_office_members = self.new_dojo.rooms['offices'][new_office_location].r_occupants
        # Check if the person is in the new room
        self.assertIn(new_person, new_office_members)

    def test_print_unallocated(self):
        """
        Test that the program prints the unallocated individuals
        The function should also write the output to file
        """
        # Create isolated instance of the object that has no rooms created
        newDojo = Dojo()
        # Add new people, no rooms exist so they go to the unallocated list
        newDojo.add_person("New", "Guy", "staff")
        newDojo.add_person("New", "Lady", "fellow", False)
        newDojo.print_unallocated("newfile.txt")
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "newfile.txt")
        # Check if file is created
        self.assertTrue(os.path.exists(file))
        with open(file) as f:
            lines = f.readlines()
            self.assertIn(" New Guy - staff\n", lines)
            self.assertIn(" New Lady - fellow\n", lines)
        os.remove(file)

    def test_save_state(self):
        """
        Test that data can be saved from the system to the database
        """
        new_db = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "new_db.db")
        self.new_dojo.save_state(new_db)

        # database file existence
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "new_db.db")))
        os.remove(new_db)

    def test_load_state(self):
        """
        Test that data can be loaded to the application from the database
        """
        # Save current data to database
        self.new_dojo.create_room("Hello", "office")
        new_db = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "new_db.db")
        self.new_dojo.save_state(new_db)

        # Get the database file and load it and check if our data was saved
        new_db = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "new_db.db")
        self.new_dojo.load_state(new_db)

        # Check if database file is found
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", "new_db.db")))

        # Data is entered into the application
        total_rooms = len(self.new_dojo.rooms['offices']) + len(self.new_dojo.rooms['livingspaces'])
        total_people = len(self.new_dojo.people['fellows']) + len(self.new_dojo.people['staff'])

        # Assert that the number of people and rooms in database is
        # equal to the number that we created when setting up the class
        self.assertEqual(3, total_rooms)
        self.assertEqual(1, total_people)

        # Check if our created office was saved and retrieved
        loaded_offices = [office.r_name for office in self.new_dojo.rooms["offices"]]
        self.assertIn("Hello", loaded_offices)

        os.remove(new_db)


if __name__ == "__main__":
    unittest.main()
