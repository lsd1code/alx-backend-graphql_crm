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
        fields = ('id', 'name', 'email', 'phone')


class CustomerInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')


class OrderType(DjangoObjectType):
    customer = graphene.Field(CustomerType)
    products = graphene.List(ProductType)

    class Meta:
        model = Order
        fields = ('id', 'order_date')


class Query(graphene.ObjectType):
    hello = graphene.String()
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    get_customer = graphene.Field(CustomerType, id=graphene.Int())
    get_product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_get_customer(root, info, id):  # type:ignore
        return Customer.objects.get(pk=id)

    def resolve_get_product(root, info, id):  # type:ignore
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


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    customers = graphene.List(lambda: CustomerType)

    @classmethod
    def mutate(cls, root, info, customers):
        customer_instances = [
            Customer(name=c.name, email=c.email, phone=c.phone) for c in customers
        ]

        created_customers = Customer.objects.bulk_create(customer_instances)

        return BulkCreateCustomers(customers=created_customers)  # type:ignore


class ProductInput(graphene.InputObjectType):
    product_id = graphene.Int()


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID()
        product_ids = graphene.List(ProductInput)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, customer_id):
        order = Order(customer_id=customer_id)
        order.save()

        return CreateOrder()  # type:ignore


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_customer = CreateCustomer.Field()
    bulk_create_customer = BulkCreateCustomers.Field()

    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
