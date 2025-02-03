class CategoryDataManager:
    def __init__(self, debug_logger):
        self.debug_logger = debug_logger
        self.parent_categories = {}  # {group_name: [parent_categories]}
        self.child_categories = {}   # {parent_category: [child_categories]}
        self.selected_group = None
        
    def set_selected_group(self, group_name):
        self.debug_logger.log_method_call("set_selected_group", group_name=group_name)
        self.selected_group = group_name
        if group_name not in self.parent_categories:
            self.parent_categories[group_name] = []
        return True
        
    def get_parent_categories(self, group_name=None):
        group = group_name or self.selected_group
        return self.parent_categories.get(group, [])
        
    def get_child_categories(self, parent_name):
        return self.child_categories.get(parent_name, [])