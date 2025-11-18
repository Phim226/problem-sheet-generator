from tkinter import Event, messagebox, Tk
from ttkbootstrap import Button, Entry, Frame, Scrollbar, Treeview
from core.question.question import Question
from core.question.question_registry import TOPIC_REGISTRY, QUESTION_REGISTRY

# TODO: Improve docstrings.
# TODO: Have # questions be for the current level only.
class QuestionSelector():

    QUESTION_TREE_CONFIG: dict[str, str | bool] = {
        "title": "Question Topics",
        "tree_id": "questions_tree",
        "button_label": "add",
        "has_count_column": False
    }

    SELECTED_TREE_CONFIG: dict[str, str | bool] = {
        "title": "Selected Topics",
        "tree_id": "selected_questions_tree",
        "button_label": "remove",
        "has_count_column": True
    }

    def __init__(self, root: Tk):
        self._root = root
        self._selector_frame = Frame(root)
        self._selector_frame.pack(side = "top", anchor = "nw")
        self._selected_question_ids: set[str] = set()

    @property
    def question_tree(self) -> Treeview:
        return self._question_tree

    @property
    def selected_tree(self) -> Treeview:
        return self._selected_tree

    @property
    def question_tree_id(self) -> str:
        return self.QUESTION_TREE_CONFIG["tree_id"]

    @property
    def selected_tree_id(self) -> str:
        return self.SELECTED_TREE_CONFIG["tree_id"]

    def build(self) -> None:
        self._question_tree: Treeview = self._build_tree(self.QUESTION_TREE_CONFIG)
        self._selected_tree: Treeview = self._build_tree(self.SELECTED_TREE_CONFIG)

        self._populate_question_tree(self._question_tree)

    @staticmethod
    def _populate_question_tree(tree: Treeview) -> None:
        """
        Fills the Question Topics tree with the questions, topics and subtopics that have been
        registered in the Question and Topic registries.
        """
        question_types: list[Question] = sorted(list(TOPIC_REGISTRY.keys())[1:])
        for name in question_types:
            tree.insert("", "end", iid = name, text = name)

            topics = QUESTION_REGISTRY[name].subtopics.keys()
            for topic in topics:
                tree.insert(name, "end", iid = topic, text = topic)

                subtopics = TOPIC_REGISTRY[name][topic]
                for subtopic in subtopics:
                    tree.insert(topic, "end", iid = f"{topic}_{subtopic}", text = subtopic)


    def _build_tree(self, config: dict[str, str | bool]) -> Treeview:
        """
        Builds the tree and button UI widgets for the given configuration.
        """
        tree_frame: Frame = Frame(self._selector_frame)
        tree_frame.pack(side = "left")

        command = self._add if config["button_label"] == "add" else self._remove
        button = Button(tree_frame, text = config["button_label"], command = command)
        button.tree_button_id = config["tree_id"]
        button.pack(side = "bottom", anchor = "se")

        columns = ("count",) if config["has_count_column"] else None
        tree = Treeview(tree_frame, columns = columns, show = "tree headings")
        tree.heading("#0", text = config["title"])

        if config["has_count_column"]:
            tree.heading("count", text = "#Qs")
            tree.column("count", width = 60, anchor = "center", stretch = False)

            tree.bind("<Double-1>", self._edit_count)

        tree.pack(side = "left")

        vertical_scroll = Scrollbar(tree_frame, orient = "vertical", command = tree.yview)
        vertical_scroll.pack(side = "right", fill = "y")
        tree.configure(yscrollcommand = vertical_scroll.set)

        return tree

    def _edit_count(self, event: Event) -> None | str:
        """
        Creates an entry box at the position of a valid #Qs column cell and overrides current
        numerical value with the inputted value.
        """
        column = self._selected_tree.identify_column(event.x)
        if column != "#1":
            return

        row_id = self._selected_tree.identify_row(event.y)
        if not row_id:
            return

        current = self._selected_tree.set(row_id, "count")

        bbox = self._selected_tree.bbox(row_id, column)
        if not bbox:
            return "break"

        x, y, width, height = bbox

        pad_x = 2
        pad_y = 2
        width = max(width, 50)
        height = height + pad_y

        entry = Entry(self._selected_tree)
        entry.insert(0, current)
        entry.select_range(0, "end")
        entry.focus_set()

        entry.place(
            x = x - pad_x,
            y = y - pad_y//2,
            width = width + 2*pad_x,
            height = height + pad_y
        )

        committed = False
        def commit(event: Event = None) -> None:
            nonlocal committed
            if committed:
                committed = False
                return
            committed = True

            new_val = entry.get().strip()

            while True:
                try:
                    int(new_val)
                    break
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid input")
                    return
            if new_val == "":
                new_val = "-"
            self._selected_tree.set(row_id, "count", new_val)
            entry.destroy()

        def cancel(event: Event = None) -> None:
            entry.destroy()

        entry.bind("<Return>", commit)
        entry.bind("<FocusOut>", commit)
        entry.bind("<Escape>", cancel)

        return "break"

    def _get_all_parents(self, tree: Treeview, item_id: str, parents: list[str] | None = None) -> list[str]:
        """
        Returns the chain of parent items from item_id up to the root item.
        """
        if parents is None:
            parents: list[str] = []

        parent = tree.parent(item_id)

        if not parent:
            return parents

        parents.append(parent)
        return self._get_all_parents(tree, parent, parents)

    def _get_subtree_ids(self, tree: Treeview, item_id: str, children: list[str] | None = None) -> list[str]:
        """
        Returns the full list of item ids in the subtree with item_id acting as the root node.
        """
        if children is None:
            children: list[str] = []

        children.append(item_id)

        item_children = list(tree.get_children(item_id))

        if not item_children:
            return children

        for child in item_children:
            self._get_subtree_ids(tree, child, children)

        return children

    def _count_leaves(self, tree: Treeview, item_id: str, num_children: int = 0) -> int:
        """
        Counts the number of question subtopics in the subtree of item_id.
        """
        item_children = list(tree.get_children(item_id))

        if not item_children:
            num_children += 1
            return num_children

        for child in item_children:
            num_children = self._count_leaves(tree, child, num_children)

        return num_children

    def _copy_item(
            self, src_tree: Treeview, dest_tree: Treeview, item_id: str, parent_id: str, item_open: bool
    ) -> None:
        """
        Copies item_id from the source tree to the destination tree.
        """
        if item_id in dest_tree.get_children(parent_id):
            return

        text = src_tree.item(item_id)["text"]
        dest_tree.insert(parent_id, "end", iid = item_id, text = text, values = "-", open = item_open)

    def _copy_subtree(
            self, src_tree: Treeview, dest_tree: Treeview, item_id: str, parent_id: str = "",
    ) -> None:
        """
        Copies the full subtree with item_id as the root node from the source tree to the
        destination tree.
        """
        self._copy_item(src_tree, dest_tree, item_id, parent_id, False)

        item_children = src_tree.get_children(item_id)
        for child_id in item_children:
            self._copy_subtree(src_tree, dest_tree, child_id, item_id)

    def _add(self) -> None:
        """
        Adds the selected items from the Question Topics tree to the Selected Topics tree, and
        keeps track of the selected items.
        """
        selection: list[str] = list(self._question_tree.selection())
        if not selection:
            return

        for item_id in selection:
            if item_id in self._selected_question_ids:
                continue

            item_parents = self._get_all_parents(self._question_tree, item_id)
            item_parents.reverse()

            for i, parent in enumerate(item_parents):
                if parent in self._selected_question_ids:
                    continue

                parent_id = "" if i == 0 else item_parents[i-1]
                self._copy_item(self._question_tree, self._selected_tree, parent, parent_id, True)
                self._selected_question_ids.add(parent)

            parent_id = self._question_tree.parent(item_id)
            self._copy_subtree(self._question_tree, self._selected_tree, item_id, parent_id)

            subtree_ids = self._get_subtree_ids(self._question_tree, item_id)
            self._selected_question_ids.update(subtree_ids)

            count = self._count_leaves(self._question_tree, item_id)
            self._selected_tree.set(item_id, "count", count)

    def _remove(self) -> None:
        """
        Deletes the selected items from the Selected Topics tree and from the tracked items.
        """
        selection: list[str] = list(self._selected_tree.selection())
        if not selection:
            return

        for item_id in selection:
            if item_id not in self._selected_question_ids:
                continue

            subtree_ids = self._get_subtree_ids(self._selected_tree, item_id)
            self._selected_question_ids = self._selected_question_ids - set(subtree_ids)

            parents = self._get_all_parents(self._selected_tree, item_id)
            self._selected_tree.delete(item_id)

            for parent in parents:
                if parent and not self._selected_tree.get_children(parent):
                    self._selected_tree.delete(parent)
                    self._selected_question_ids.remove(parent)
