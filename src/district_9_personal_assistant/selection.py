from typing import List, Any
import questionary


class Selection:
    @staticmethod
    def select_item_interactively(
            items: List[Any],
            display_func,
            message: str,
    ) -> Any:
        if not items:
            return None
        if len(items) == 1:
            return items[0]
        choices = [f"{idx}: {display_func(item)}" for idx, item in enumerate(items)]
        selected = questionary.select(message, choices=choices).ask()
        if not selected:
            return None
        selected_idx = int(selected.split(":")[0])
        return items[selected_idx]
