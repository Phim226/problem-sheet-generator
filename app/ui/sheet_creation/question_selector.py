from dataclasses import dataclass, field
from uuid import uuid4
from tkinter import Event, messagebox, Tk
from ttkbootstrap import Button, Entry, Frame, Scrollbar, Treeview
from core.question.question import Question
from core.question.question_registry import TOPIC_REGISTRY

@dataclass(slots = True)
class QuestionConfig():

    _id: str = field(default_factory=lambda: str(uuid4()), init=False)
    _topics: list[str | None] = field(init=False)
    num_questions: int = 1

    def __init__(self, topics: list[str | None], num_questions: int = 1):
        object.__setattr__(self, "_id", str(uuid4()))
        object.__setattr__(self, "_topics", topics)
        self.num_questions = num_questions

    @property
    def id(self):
        return self._id

    @property
    def topics(self):
        return self._topics

# TODO: Improve docstrings.
# TODO: Display text of question instead of ids.
class QuestionSelector():

    QUESTION_TREE_CONFIG: dict[str, str | bool] = {
        "title": "Question Topics",
        "tree_id": "questions_tree",
        "button_label": "add",
        "has_count_column": False
    }

    SELECTED_TREE_CONFIG: dict[str, str | bool] = {
        "title": "Selected Questions",
        "tree_id": "selected_questions_tree",
        "button_label": "remove",
        "has_count_column": True
    }

    def __init__(self, root: Tk):
        self._root = root
        self._selector_frame = Frame(root)
        self._selector_frame.pack(side = "top", anchor = "nw")
        self._selected_questions: dict[str, QuestionConfig] = {}

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

    @property
    def selected_questions(self) -> dict[str, QuestionConfig]:
            return self._selected_questions

    def build(self) -> None:
        self._question_tree: Treeview = self._build_tree(self.QUESTION_TREE_CONFIG)
        self._selected_tree: Treeview = self._build_tree(self.SELECTED_TREE_CONFIG)

        self._populate_question_tree(self._question_tree)

    @staticmethod
    def _populate_question_tree(tree: Treeview) -> None:
        """
        Fills the Question Topics tree with the questions, topics and subtopics that have been
        registered in the topic registry.
        """
        question_types: list[Question] = sorted(list(TOPIC_REGISTRY.keys())[1:])
        for name in question_types:
            tree.insert("", "end", iid = name, text = name)

            topics = TOPIC_REGISTRY[name].keys()
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

        # TODO: Have 0 call _remove, with warning
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

                    if new_val == "":
                        raise ValueError

                    new_val_int = int(new_val)

                    if new_val_int < 0:
                        raise ValueError

                    break
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid input")
                    return

            self._selected_questions[row_id].num_questions = new_val_int
            self._selected_tree.set(row_id, "count", new_val)
            entry.destroy()

        def cancel(event: Event = None) -> None:
            entry.destroy()

        entry.bind("<Return>", commit)
        entry.bind("<FocusOut>", commit)
        entry.bind("<Escape>", cancel)

        return "break"

    def _get_all_parents(
            self, tree: Treeview, item_id: str, parents: list[str] | None = None
    ) -> list[str]:
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

    def _get_subtree_ids(
            self, tree: Treeview, item_id: str, children: list[str] | None = None
    ) -> list[str]:
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
            self,
            src_tree: Treeview,
            dest_tree: Treeview,
            item_id: str,
            parent_id: str,
            item_open: bool,
            config_id: str
    ) -> None:
        """
        Copies item_id from the source tree to the destination tree.
        """
        if item_id in dest_tree.get_children(parent_id):
            return

        text = src_tree.item(item_id)["text"]
        dest_tree.insert(parent_id, "end", iid = config_id, text = text, values = "-", open = item_open)

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

            parents = reversed(self._get_all_parents(self._question_tree, item_id))

            topics = [None, None, None]
            if parents:
                i = 0
                for parent in parents:
                    topics[i] = parent
                    i += 1
                topics[i] = item_id
            else:
                topics[0] = item_id

            config = QuestionConfig(topics)
            self._copy_item(self._question_tree, self._selected_tree, item_id, "", False, config.id)
            self._selected_questions[config.id] = config
            self._selected_tree.set(config.id, "count", 1)

    def _remove(self) -> None:
        """
        Deletes the selected items from the Selected Topics tree and from the tracked items.
        """
        selection: list[str] = list(self._selected_tree.selection())
        if not selection:
            return

        for item_id in selection:
            if item_id not in self._selected_questions:
                continue

            self._selected_tree.delete(item_id)
            self._selected_questions.pop(item_id)