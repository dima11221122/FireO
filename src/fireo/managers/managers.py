from fireo.queries import query_set as queries


class ManagerError(Exception):
    pass


class ManagerDescriptor:
    """Restrict user to get `Manager` from model instance"""
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise ManagerError(f"Manager {self.manager.name} can not accessible via {owner.__name__} instance")
        return self.manager


class Manager:
    """Manager are used to perform firestore action directly from model class without instance

    Default manager can be accessible via `collection` from model class

    Examples
    -------
    .. code-block:: python
        class User(Model):
            name = TextField()

        user = User.collection.create(name="Azeem")

    Attributes
    ----------
    queryset:
        Read only property, provide operations related to firestore

    Methods
    -------
    mutable_model(model):
        Make changes in existing model instance

    contribute_to_model(model_cls, name="collection"):
        Attach manager to model class

    create(kwargs):
        create new document in firestore collection

    get(id):
        Get document from firestore
    """
    def __init__(self):
        self.model = None
        self.name = None

    def mutable_model(self, model):
        """Make changes in existing model instance

        After performing firestore action modified this instance
        adding things init like id etc
        """
        self.model = model

    def contribute_to_model(self, model_cls, name="collection"):
        """Attach manager to model class

        This method attach manager to model class

        Parameters
        ----------
        model_cls : Model
            In which model this manager will be attached

        name : str
            What is the name of this manager when it is attaching with model and
            later can be accessible with this name
        """
        self.name = name
        self.model = model_cls
        setattr(model_cls, name, ManagerDescriptor(self))

    @property
    def queryset(self):
        """provide operations related to firestore"""
        return queries.QuerySet(self.model)

    def create(self, **kwargs):
        """create new document in firestore collection"""
        return self.queryset.create(**kwargs)

    def get(self, id):
        """Get document from firestore"""
        return self.queryset.get(id)