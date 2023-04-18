from django.core.validators import MaxValueValidator, MinValueValidator

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User
from users.validators import validate_name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        title = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        if (
            self.context.get('request').method == 'POST'
            and Review.objects.filter(author=author, title=title).exists()
        ):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class TitleGETSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        reviews = Review.objects.filter(title_id=obj.id)
        total_scores = [review.score for review in reviews]
        if not total_scores:
            return None
        rating = round(sum(total_scores) / len(total_scores))
        return rating


class TitlePOSTSerializer(TitleGETSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta(TitleGETSerializer.Meta):
        pass


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r"^[^\W\d]\w*$",
        validators=[
            validate_name,
        ]
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def validate(self, data):
        if User.objects.filter(
                email=data['email']).exists() and User.objects.filter(
                username=data['username']).exists():
            return data
        if User.objects.filter(
                email=data['email']).exists():
            raise serializers.ValidationError("status.HTTP_400_BAD_REQUEST")
        if User.objects.filter(
                username=data['username']).exists():
            raise serializers.ValidationError("status.HTTP_400_BAD_REQUEST")
        return data

    class Meta:
        fields = ('email', 'username')
        model = User


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User
