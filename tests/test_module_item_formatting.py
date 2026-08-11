import unittest

from canvas_ed_mcp import format_module_items_markdown


class ModuleItemFormattingTests(unittest.TestCase):
    def test_file_item_exposes_canvas_file_id(self) -> None:
        result = format_module_items_markdown(
            [
                {
                    "id": 3206862,
                    "content_id": 987654,
                    "type": "File",
                    "title": "INFO6007 Group Assignment Overview.pdf",
                    "html_url": (
                        "https://canvas.example.edu/courses/73754/"
                        "modules/items/3206862"
                    ),
                }
            ],
            "Group Project",
        )

        self.assertIn("**Item ID**: 3206862", result)
        self.assertIn("**File ID**: 987654", result)
        self.assertIn("canvas_get_file_content", result)
        self.assertIn("canvas_download_file", result)

    def test_non_file_item_does_not_claim_content_id_is_a_file_id(self) -> None:
        result = format_module_items_markdown(
            [
                {
                    "id": 3129663,
                    "content_id": 123456,
                    "type": "Page",
                    "title": "Assessment overview",
                }
            ]
        )

        self.assertNotIn("**File ID**", result)


if __name__ == "__main__":
    unittest.main()
