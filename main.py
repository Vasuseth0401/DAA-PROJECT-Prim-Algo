
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.network_manager import NetworkManager


network = NetworkManager()

while True:

    print("\n===== NETOPTIMA =====")
    print("1. Add Location")
    print("2. Add Connection")
    print("3. Display Network")
    print("4. Save Network")
    print("5. Load Network")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    try:

        if choice == "1":

            location = input("Enter location name: ")
            network.add_location(location)

            print("Location added successfully!")

        elif choice == "2":

            location1 = input("Enter first location: ")
            location2 = input("Enter second location: ")

            cost = float(input("Enter installation cost: "))

            network.add_connection(
                location1,
                location2,
                cost
            )

            print("Connection added successfully!")

        elif choice == "3":

            network.display_network()

        elif choice == "4":

            network.save_network()

        elif choice == "5":

            network.load_network()

        elif choice == "6":

            print("Exiting NetOptima...")
            break

        else:

            print("Invalid choice!")

    except (ValueError, OSError) as error:

        print("Error:", error)
