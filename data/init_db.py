import os
import json
import sys

# Đảm bảo import được từ thư mục gốc
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from infrastructure.persistence.sqlite_repository_adapter import SqliteRepositoryAdapter
from domain.entities.content_item import ContentItem, LaunchStrategy, AvailabilityStatus


def init_database(db_path: str = "data/context_db.sqlite", seed_file: str = "data/catalog_seed.json"):
    print(f"[*] Khởi tạo SQLite Database tại: {db_path}")
    repo = SqliteRepositoryAdapter(db_path)

    if not os.path.isfile(seed_file):
        seed_file = os.path.join(base_dir, seed_file)

    if os.path.isfile(seed_file):
        with open(seed_file, "r", encoding="utf-8") as f:
            catalog_data = json.load(f)

        count = 0
        for item in catalog_data:
            c_item = ContentItem(
                id=item["id"],
                name=item["name"],
                category=item["category"],
                provider=item["provider"],
                launch_strategy=LaunchStrategy(item.get("launch_strategy", "DIRECT_DEEPLINK")),
                deep_link=item.get("deep_link"),
                speaker_or_artist=item.get("speaker_or_artist"),
                tags=item.get("tags", []),
                default_priority=item.get("default_priority", 50)
            )
            repo.save(c_item)
            count += 1
        print(f"[✓] Đã nạp thành công {count} nội dung quen thuộc vào Content Catalog!")
    else:
        print(f"[!] Không tìm thấy file seed: {seed_file}")


if __name__ == "__main__":
    init_database()

