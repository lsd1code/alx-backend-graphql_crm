import graphene
from graphene_django import DjangoObjectType

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import (
    Product, Customer, Order
)


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')


class Query(graphene.ObjectType):
    hello = graphene.String()
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(CustomerType)
    get_customer = graphene.Field(CustomerType, id=graphene.Int())
    get_product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_get_customer(root, info, id):
        return Customer.objects.get(pk=id)

    def resolve_get_product(root, info, id):
        return Product.objects.get(pk=id)

    def resolve_all_customers(root, info):  # type:ignore
        return Customer.objects.all()

    def resolve_all_products(root, info):  # type:ignore
        return Product.objects.all()

    def resolve_hello(root, info):  # type:ignore
        return "Hello, GraphQL!"


class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)

    class Arguments:
        name = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    @classmethod
    def mutate(cls, root, info, name, email, phone):
        try:
            validate_email(email)
        except ValidationError:
            raise Exception("Invalid email address")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)  # type: ignore


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String()
        price = graphene.Decimal()
        stock = graphene.Int()

    @classmethod
    def mutate(cls, root, info, name, price, stock):
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)  # type: ignore


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_customer = CreateCustomer.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
