import graphene


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):  # type:ignore
        return "Hello, GraphQL!"


schema = graphene.Schema(query=Query)
