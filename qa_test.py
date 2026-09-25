#!/usr/bin/env python3
"""
Flow Desk QA Testing Script
Comprehensive verification of halls, services, photos, and games
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "https://universal.flow-desk.ru/mcp"
API_KEY = "fdmcp_v1_3cj4fKeQRW6rbdWWZ3BdsY3fTd7auZCyAiQJ8JqS3Hg"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Expected data
EXPECTED_HALLS = 15
EXPECTED_SERVICES = 51
EXPECTED_GAMES = 10

HALL_NAMES = [
    "Розовый сад",
    "Фламинго",
    "Sakura",
    "Pink Dreams",
    "Персиковая роза",
    "Magnolia",
    "Нежность",
    "Rose Garden",
    "Красотка",
    "Pink Velvet",
    "Королевская роза",
    "Sunset",
    "Pink Palace",
    "Серенада",
    "Империя розы"
]

EXPECTED_PRICES = list(range(1000, 16000, 1000))

GAMES = [
    "Мафия",
    "Бункер",
    "Квиз",
    "Музыкальное лото",
    "Алиби",
    "Активити",
    "Крокодил",
    "Имаджинариум",
    "Скраббл",
    "Монополия"
]

class QATester:
    def __init__(self):
        self.report = []
        self.passed = 0
        self.failed = 0

    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {status}: {message}"
        print(log_line)
        self.report.append(log_line)

    def test_passed(self, test_name):
        self.passed += 1
        self.log(f"✓ {test_name}", "PASS")

    def test_failed(self, test_name, reason=""):
        self.failed += 1
        self.log(f"✗ {test_name} - {reason}", "FAIL")

    def run_tests(self):
        self.log("=" * 60)
        self.log("FLOW DESK QA TEST SUITE STARTED")
        self.log("=" * 60)

        # Test 1: Fetch and verify halls
        self.test_halls()

        # Test 2: Fetch and verify services
        self.test_services()

        # Test 3: Verify photos
        self.test_photos()

        # Test 4: Generate report
        self.generate_report()

    def test_halls(self):
        self.log("-" * 60)
        self.log("TEST 1: HALL VERIFICATION")
        self.log("-" * 60)

        try:
            response = requests.get(
                f"{BASE_URL}/booking-api/admin/halls",
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                self.test_failed(
                    "Fetch all halls",
                    f"HTTP {response.status_code}: {response.text[:100]}"
                )
                return

            halls = response.json()

            # Check count
            if len(halls) == EXPECTED_HALLS:
                self.test_passed(f"Hall count verification (found {len(halls)} halls)")
            else:
                self.test_failed(
                    f"Hall count verification",
                    f"Expected {EXPECTED_HALLS}, found {len(halls)}"
                )

            # Check names and prices
            names_ok = 0
            prices_ok = 0
            photos_ok = 0

            for i, hall in enumerate(halls, 1):
                hall_id = hall.get('adminId', i)
                hall_name = hall.get('name', '')
                hall_price = hall.get('price', 0)
                photo_url = hall.get('photoUrl', '')

                # Verify name
                if i <= len(HALL_NAMES) and hall_name == HALL_NAMES[i-1]:
                    names_ok += 1
                else:
                    self.log(
                        f"  Hall {i}: Name mismatch - Expected '{HALL_NAMES[i-1]}', "
                        f"got '{hall_name}'",
                        "WARN"
                    )

                # Verify price
                expected_price = EXPECTED_PRICES[i-1] if i <= len(EXPECTED_PRICES) else None
                if hall_price == expected_price:
                    prices_ok += 1
                else:
                    self.log(
                        f"  Hall {i}: Price mismatch - Expected {expected_price}₽, "
                        f"got {hall_price}₽",
                        "WARN"
                    )

                # Verify photo
                if photo_url and "unsplash" in photo_url.lower():
                    photos_ok += 1
                else:
                    self.log(
                        f"  Hall {i}: Photo missing or invalid - {photo_url}",
                        "WARN"
                    )

                self.log(f"  Hall {i}: {hall_name} - {hall_price}₽ - Photo: {'✓' if photo_url else '✗'}")

            self.log(f"  Names correct: {names_ok}/{len(halls)}")
            self.log(f"  Prices correct: {prices_ok}/{len(halls)}")
            self.log(f"  Photos assigned: {photos_ok}/{len(halls)}")

            if names_ok == len(halls) and prices_ok == len(halls) and photos_ok == len(halls):
                self.test_passed("All halls configured correctly")
            else:
                self.test_failed(
                    "Hall configuration",
                    f"Names: {names_ok}, Prices: {prices_ok}, Photos: {photos_ok}"
                )

        except Exception as e:
            self.test_failed("Fetch all halls", str(e))

    def test_services(self):
        self.log("-" * 60)
        self.log("TEST 2: SERVICES VERIFICATION")
        self.log("-" * 60)

        try:
            response = requests.get(
                f"{BASE_URL}/booking-api/admin/services",
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                self.test_failed(
                    "Fetch all services",
                    f"HTTP {response.status_code}: {response.text[:100]}"
                )
                return

            services = response.json()

            # Check count
            if len(services) == EXPECTED_SERVICES:
                self.test_passed(f"Service count verification (found {len(services)} services)")
            else:
                self.test_failed(
                    "Service count verification",
                    f"Expected {EXPECTED_SERVICES}, found {len(services)}"
                )

            # Check for games
            games_found = []
            for service in services:
                service_name = service.get('name', '')
                for game in GAMES:
                    if game.lower() in service_name.lower():
                        games_found.append(game)
                        break

            self.log(f"  Total services: {len(services)}")
            self.log(f"  Games found: {len(games_found)}/{EXPECTED_GAMES}")

            if len(games_found) == EXPECTED_GAMES:
                self.test_passed(f"All {EXPECTED_GAMES} games found in services")
            else:
                self.test_failed(
                    "Games verification",
                    f"Expected {EXPECTED_GAMES} games, found {len(games_found)}"
                )
                self.log(f"  Found games: {games_found}", "WARN")
                missing = set(GAMES) - set(games_found)
                if missing:
                    self.log(f"  Missing games: {missing}", "WARN")

            # List all service categories
            categories = {}
            for service in services:
                category = service.get('category', 'Uncategorized')
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1

            self.log("  Service categories:")
            for category, count in sorted(categories.items()):
                self.log(f"    - {category}: {count}")

        except Exception as e:
            self.test_failed("Fetch all services", str(e))

    def test_photos(self):
        self.log("-" * 60)
        self.log("TEST 3: PHOTOS VERIFICATION")
        self.log("-" * 60)

        try:
            response = requests.get(
                f"{BASE_URL}/booking-api/admin/halls",
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                self.test_failed("Fetch halls for photo check", f"HTTP {response.status_code}")
                return

            halls = response.json()
            photos_with_url = 0

            for hall in halls:
                if hall.get('photoUrl'):
                    photos_with_url += 1

            self.log(f"  Halls with photos: {photos_with_url}/{len(halls)}")

            if photos_with_url == len(halls):
                self.test_passed("All halls have photo URLs assigned")
            else:
                self.test_failed(
                    "Photo assignment",
                    f"{photos_with_url}/{len(halls)} halls have photos"
                )

        except Exception as e:
            self.test_failed("Photos verification", str(e))

    def generate_report(self):
        self.log("-" * 60)
        self.log("QA TEST SUMMARY")
        self.log("-" * 60)
        self.log(f"Tests Passed: {self.passed}")
        self.log(f"Tests Failed: {self.failed}")
        self.log(f"Total: {self.passed + self.failed}")

        if self.failed == 0:
            self.log("=" * 60)
            self.log("✓ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION")
            self.log("=" * 60)
        else:
            self.log("=" * 60)
            self.log("✗ SOME TESTS FAILED - REVIEW REQUIRED")
            self.log("=" * 60)

        # Save report
        report_file = "/home/user/kp/QA_REPORT.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.report))

        self.log(f"Report saved to: {report_file}")

def main():
    tester = QATester()
    tester.run_tests()

if __name__ == "__main__":
    main()
