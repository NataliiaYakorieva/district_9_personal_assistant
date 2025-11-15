from typing import List, Any, Callable, Optional
import questionary


class Selection:
    """
    Provides interactive selection functionality for lists of items.
    """

    @staticmethod
    def select_item_interactively(
            items: List[Any],
            display_func: Callable[[Any], str],
            message: str,
    ) -> Optional[Any]:
        """
        Interactively select an item from a list using questionary.
        Returns the selected item, or None if no selection is made.
        """
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
