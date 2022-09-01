import threading


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def registry_new(self, object):
        self.new_objects.append(object)

    def register_dirty(self, object):
        self.dirty_objects.append(object)

    def register_removed(self, object):
        self.removed_objects.append(object)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        print(self.new_objects)
        for item in self.new_objects:
            print(f'MapperRegistry: {self.MapperRegistry}')
            self.MapperRegistry.get_mapper(item).inser(object)

    def delete_removed(self):
        for item in self.removed_objects:
            self.MapperRegistry.get_mapper(item).delete(item)

    def update_dirty(self):
        for item in self.dirty_objects:
            self.MapperRegistry.get_mapper(item).update(item)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
