from django.shortcuts import render
from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from sympy import Symbol, diff, integrate, limit, oo, sympify
from rest_framework import status
from .models import MathOperation, Chat
from rest_framework import serializers
from .serializers import MathRequestSerializer, ChatSerializer

class MathAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MathRequestSerializer(data=request.data)
        if serializer.is_valid():
            operation = serializer.validated_data.get('operation')
            expression = serializer.validated_data.get('expression')
            limit_value = serializer.validated_data.get('limit_value', oo)
            x_value = serializer.validated_data.get('x_value')
            upper_limit = serializer.validated_data.get('upper_limit')
            lower_limit = serializer.validated_data.get('lower_limit')

            result = self.perform_math_operation(operation, expression, limit_value)
            numerical_result = self.perform_numerical_operation(operation, expression, x_value, upper_limit, lower_limit)

            # MathOperation.objects.create(
            #     operation=operation,
            #     expression=expression,
            #     result=result,
            #     numerical_result=numerical_result,
            #     upper_limit=upper_limit,
            #     lower_limit=lower_limit,
            #     x_value=x_value
            # )

            return Response({'result': result +" + c", 'numerical_result': numerical_result})
        else:
            return Response({'error': 'Invalid data'}, status=400)

    def perform_math_operation(self, operation, expression, limit_value):
        x = Symbol('x')

        try:
            expr = sympify(expression)
        except Exception as e:
            return f'Error in expression: {str(e)}'

        if operation == 'derivative':
            return str(diff(expr, x))
        elif operation == 'integrate':
            return str(integrate(expr, x))
        elif operation == 'limit':
            try:
                result = limit(expr, x, limit_value)
                return str(result)
            except Exception as e:
                return f'Error in limit expression: {str(e)}'
        else:
            try:
                result = eval(f'{operation}({expr})')
                return str(result)
            except Exception as e:
                return f'Error in operation: {str(e)}'

    def perform_numerical_operation(self, operation, expression, x_value, upper_limit, lower_limit):
        x = Symbol('x')

        try:
            expr = sympify(expression)
        except Exception as e:
            return f'Error in expression: {str(e)}'

        if operation == 'derivative':
            return self.calculateDerivativeWithValue(expr, x, x_value)
        elif operation == 'integrate':
            return self.calculateDefiniteIntegral(expr, x, upper_limit, lower_limit)
        else:
            return self.calculateAnotherOperation(operation, expr)

    def calculateDerivativeWithValue(self, expr, x, x_value):
        if x_value is not None:
            try:
                result = diff(expr, x).subs(x, x_value)
                return str(result)
            except Exception as e:
                return f'Error during calculation: {str(e)}'
        else:
            return None

    def calculateDefiniteIntegral(self, expr, x, upper_limit, lower_limit):

        if upper_limit is not None and lower_limit is not None:
            try:
                integral = integrate(expr, (x, lower_limit, upper_limit))
                return str(integral)
            except Exception as e:

                return f'Error during integration: {str(e)}'
        else:
            return None

    def calculateAnotherOperation(self, operation, expr):
        try:
            result = eval(f'{operation}({expr})')
            return str(result)
        except Exception as e:
            return f'Error in operation: {str(e)}'
        
class ChatAPIView(APIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
