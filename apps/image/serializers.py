from rest_framework import serializers
from django.core.validators import FileExtensionValidator, get_available_image_extensions


# django内置的一个函数,获取可用的图片后缀名
# print(get_available_image_extensions())


class UploadImageSerializer(serializers.Serializer):
    # ImageField：会校验上传的文件是否是图片
    # 1.要验证图片是正确的图片,而不是改了后缀名的 例如 xx.py改为xx.jpg,这是不允许的
    # 2.验证只允许特定格式的图片上传,只允许 jpg,jpeg,png,gif
    image = serializers.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
                                   error_messages={'required': '请上传图片!', 'invalid_image': '请上传正确格式的图片！'})

    # 只允许上传0.5M以内大小的图片
    def validate_image(self, value):
        max_size = 0.5 * 1024 * 1025
        # 获取上传图片的大小,单位是字节
        size = value.size
        # 如果上传的图片大小大于0.5M,抛出异常
        if size > max_size:
            raise serializers.ValidationError('图片最大不能超过0.5MB！')
        return value
