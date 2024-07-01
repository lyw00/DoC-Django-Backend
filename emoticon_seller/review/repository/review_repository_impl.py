import os

from review.entity.models import Review
from review.repository.review_repository import ReviewRepository
from emoticon_seller import settings


class ReviewRepositoryImpl(ReviewRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Review.objects.all().order_by('reviewRegDate')

    def register(self, reviewTitle, reviewWriter, reviewContent,reviewRating,reviewImage):
        uploadDirectory = os.path.join(
            settings.BASE_DIR,
            '../../DoC-Vue-Frontend/src/assets/images/uploadImages'
        )
        if not os.path.exists(uploadDirectory):
            os.makedirs(uploadDirectory)
        if reviewImage:
            imagePath = os.path.join(uploadDirectory, reviewImage.name)
            with open(imagePath, 'wb+') as destination:
                for chunk in reviewImage.chunks():
                    destination.write(chunk)

                destination.flush()
                os.fsync(destination.fileno())

            review = Review(
                reviewTitle=reviewTitle,
                reviewWriter=reviewWriter,
                reviewContent=reviewContent,
                reviewRating=reviewRating,
                reviewImage=reviewImage.name,
            )
        else:
            review = Review(
                reviewTitle=reviewTitle,
                reviewWriter=reviewWriter,
                reviewContent=reviewContent,
                reviewRating=reviewRating,
                reviewImage=None,
            )
        review.save()
        return review

