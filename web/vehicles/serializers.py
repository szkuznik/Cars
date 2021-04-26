import requests
from rest_framework import serializers

from vehicles.models import Car, CarRating


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']

    def validate(self, data):
        """
        Check that make with this model exists.
        """
        # ToDo In future If we want to use this api to other tasks we should move it to external module
        response = requests.get(
            f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{data.get("make")}?format=json'
        )
        if response.status_code != 200:
            raise serializers.ValidationError("External validation failed")
        for row in response.json().get("Results"):
            if row.get("Model_Name") == data.get("model"):
                break
        else:
            raise serializers.ValidationError("Make with model does not exists")
        return data


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRating
        fields = '__all__'
