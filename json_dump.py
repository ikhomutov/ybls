import json

from ybls.core import models
from ybls.core import constants


def main(level):
    with open(f'class_{level}_mongo_dump.json', 'r') as f:
        data = json.load(f)
    for subject_dict in data:
        subject, _ = models.Subject.objects.get_or_create(
            ibls_id = subject_dict['id'],
            defaults = {'name': subject_dict['name']}
        )
        for lesson_dict in subject_dict['lessons']:
            lesson, _ = models.Lesson.objects.get_or_create(
                level=level,
                subject=subject,
                index=lesson_dict['index'],
                defaults={'name': lesson_dict['name']}
            )
            for topic_dict in lesson_dict['topics']:
                for index, content_dict in enumerate(topic_dict['contents'], 1):
                    content, _ = models.Content.objects.get_or_create(
                        lesson=lesson,
                        order=index,
                        defaults={'name': content_dict['name']}
                    )
                    for index, material_dict in enumerate(content_dict['materials']):
                        material_type = material_dict['type']['id']
                        data = {}
                        if material_type == constants.MATERIAL_VIMEO:
                            data.update(link=material_dict['link'])
                        elif material_type == constants.MATERIAL_AUDIO:
                            data.update(**material_dict['file'])
                        else:
                            data.update(text=material_dict['text'])
    
                        models.Material.objects.update_or_create(
                            order=index,
                            content=content,
                            type=material_type,
                            defaults={
                                'data': data,
                            }
                        )


if __name__ == '__main__':
    main(1)
