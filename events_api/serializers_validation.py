from rest_framework import serializers


class EventSerializerValidators:

    @staticmethod
    def start_end_date(data):
        """ Check start date is before end date """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("finish must occur after start.")
        return data

    @staticmethod
    def event_weight(data):
        """ Check if event multiplier is not set too high """
        max_event_weight: float = data['event_weight']
        if max_event_weight > 5:
            raise serializers.ValidationError(f"Event points multiplier cant be more than {max_event_weight}.")
        return data


class RiderSerializerValidators:

    @staticmethod
    def check_age(data):
        """ Check age input """
        max_age: int = data['age']
        if data['age'] > 110:
            raise serializers.ValidationError(f'Check if entered age is correct. Max age is set to {max_age}')
        return data
