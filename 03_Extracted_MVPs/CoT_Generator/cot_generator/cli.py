import sys
import json
from .generator import PrePolishedCoTGenerator

def main():
    print("==================================================================")
    print("  Pre-Polished CoT Generator CLI - Enterprise Edition v2.0")
    print("==================================================================")
    print("1. Generate All Batches (1500 chains)")
    print("2. Generate Single Vertical (500 chains)")
    print("3. Exit")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        for vertical in ["GEOPOLITICAL", "FINTECH", "PHARMA"]:
            print(f"\nGeneriere {vertical}...")
            gen = PrePolishedCoTGenerator(vertical)
            batch = gen.generate(500)
            filename = f"{vertical}_batch.json"
            with open(filename, "w") as f:
                json.dump(batch, f, indent=2)
            print(f"saved to {filename}")
            
    elif choice == "2":
        print("\nAvailable Verticals: GEOPOLITICAL, FINTECH, PHARMA")
        v = input("Enter Vertical: ").strip().upper()
        try:
            gen = PrePolishedCoTGenerator(v)
            batch = gen.generate(500)
            filename = f"{v}_batch.json"
            with open(filename, "w") as f:
                json.dump(batch, f, indent=2)
            print(f"saved to {filename}")
        except Exception as e:
            print(f"Error: {e}")
            
    print("\nDone.")

if __name__ == "__main__":
    main()
