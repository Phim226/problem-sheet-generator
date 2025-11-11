from tkinter import Tk
from ttkbootstrap import Button, Frame, Scrollbar, Treeview
from core.question.question import Question
from core.question.question_registry import TOPIC_REGISTRY, QUESTION_REGISTRY

# TODO: Write docstrings.
# TODO: Implement # questions editing.
class QuestionSelecter():

    _question_tree_title: str = "Question Topics"
    _question_tree_id: str = "questions_tree"

    _selected_tree_title: str = "Selected Topics"
    _selected_tree_id: str = "selected_questions_tree"

    _selected_question_ids: set[str] = set()


    def __init__(self, root: Tk):
        self._root = root
        self._selecter_frame = Frame(root)
        self._selecter_frame.pack(side = "top", anchor = "nw")

    @property
    def question_tree(self) -> Treeview:
        return self._question_tree

    @property
    def selected_tree(self) -> Treeview:
        return self._selected_tree

    @property
    def question_tree_id(self) -> str:
        return self._question_tree_id

    @property
    def selected_tree_id(self) -> str:
        return self._selected_tree_id

    def build(self) -> None:
        self._question_tree: Treeview = self._build_question_tree(
            self._question_tree_title,
            self._question_tree_id
        )
        self._populate_question_tree(self._question_tree)

        self._selected_tree: Treeview = self._build_question_tree(
            self._selected_tree_title,
            self._selected_tree_id
        )

    @staticmethod
    def _populate_question_tree(tree: Treeview) -> None:
        question_types: list[Question] = sorted(list(TOPIC_REGISTRY.keys())[1:])
        for name in question_types:
            tree.insert("", "end", iid = name, text = name)

            topics = QUESTION_REGISTRY[name].subtopics.keys()
            for topic in topics:
                tree.insert(name, "end", iid = topic, text = topic)

                subtopics = TOPIC_REGISTRY[name][topic]
                for subtopic in subtopics:
                    tree.insert(topic, "end", iid = f"{topic}_{subtopic}", text = subtopic)


    def _build_question_tree(self, title: str, id: str) -> Treeview:
        tree_frame: Frame = Frame(self._selecter_frame)
        tree_frame.pack(side = "left")

        button = Button(
            tree_frame,
            text = "add" if title == self._question_tree_title else "remove",
            command = self._add if title == self._question_tree_title else self._remove
        )
        button.tree_button_id = id
        button.pack(side = "bottom", anchor = "se")

        tree = Treeview(
            tree_frame,
            columns = None if title == self._question_tree_title else ("count",),
            show = "tree headings"
        )
        tree.heading("#0", text = title)
        if title == self._selected_tree_title:
            tree.heading("count", text = "#Qs")
            tree.column("count", width = 60, anchor = "center", stretch = False)
        tree.pack(side = "left")

        vertical_scroll = Scrollbar(tree_frame, orient = "vertical", command = tree.yview)
        vertical_scroll.pack(side = "right", fill = "y")

        tree.configure(yscrollcommand = vertical_scroll.set)

        tree.widget_id = id

        return tree

    def _get_all_parents(self, tree: Treeview, item_id: str, parents: list[str] = None) -> list[str]:
        if parents is None:
            parents = []

        parent = tree.parent(item_id)

        if not parent:
            return parents

        parents.append(parent)
        return self._get_all_parents(tree, parent, parents)

    def _get_subtree_ids(self, tree: Treeview, item_id: str, children: list[str] = None) -> list[str]:
        if children is None:
            children = []

        children.append(item_id)

        item_children = list(tree.get_children(item_id))

        if not item_children:
            return children

        for child in item_children:
            self._get_subtree_ids(tree, child, children)

        return children

    def _count_leaves(self, tree: Treeview, item_id: str, num_children: int = 0) -> int:
        item_children = list(tree.get_children(item_id))

        if not item_children:
            num_children += 1
            return num_children

        for child in item_children:
            num_children = self._count_leaves(tree, child, num_children)

        return num_children

    def _copy_item(
            self, src_tree: Treeview, dest_tree: Treeview, item_id: str, parent_id: str
    ) -> None:
        if item_id in dest_tree.get_children(parent_id):
            return

        text = src_tree.item(item_id)["text"]
        dest_tree.insert(parent_id, "end", iid = item_id, text = text, values = "-")

    def _copy_subtree(
            self, src_tree: Treeview, dest_tree: Treeview, item_id: str, parent_id: str = ""
    ) -> None:
        self._copy_item(src_tree, dest_tree, item_id, parent_id)

        item_children = src_tree.get_children(item_id)
        for child_id in item_children:
            self._copy_subtree(src_tree, dest_tree, child_id, item_id)

    def _add(self) -> None:
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
                self._copy_item(self._question_tree, self._selected_tree, parent, parent_id)
                self._selected_question_ids.add(parent)

            parent_id = self._question_tree.parent(item_id)
            self._copy_subtree(self._question_tree, self._selected_tree, item_id, parent_id)

            subtree_ids = self._get_subtree_ids(self._question_tree, item_id)
            self._selected_question_ids.update(subtree_ids)

            count = self._count_leaves(self._question_tree, item_id)
            self._selected_tree.set(item_id, "count", count)

    def _remove(self) -> None:
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
