"""
Bully Algorithm - Leader Election Simulation
Run all 7 activities in sequence.
"""

import activity1
import activity2
import activity3
import activity4
import activity5
import activity6
import activity7


def main():
    print("=" * 60)
    print("BULLY ALGORITHM - LEADER ELECTION SIMULATION")
    print("=" * 60)

    activity1.run()
    activity2.run()
    activity3.run()
    activity4.run()
    activity5.run()
    activity6.run()
    activity7.run()

    print("\n" + "=" * 60)
    print("ALL ACTIVITIES COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
