from .models import QuestionLikes
from django.db.models import Q
from django.conf import settings

def check_like_question(user, question):
    count = QuestionLikes.objects.filter(user=user, question=question).count()
    return count > 0

def _search_by_categories(query_set, categories):
    query_set = query_set.filter(categories__category__id__in=categories)
    return query_set

def _search_by_areas(query_set, areas):
    queries = []
    for area in areas:
        province_id = area.get('province_id', None)
        city_id = area.get('city_id', None)
        area_id = area.get('area_id', None)
        station_id = area.get('station_id', None)

        conditions = []
        if province_id:
            conditions.append(Q(areas__province__id=province_id))

        if city_id:
            conditions.append(Q(areas__city__id=city_id))

        if area_id:
            conditions.append(Q(areas__area__id=area_id))

        if station_id:
            conditions.append(Q(areas__station__id=station_id))

        query = conditions.pop()
        for condition in conditions:
            query &= condition

        queries.append(query)

    query = queries.pop()
    for condition in queries:
        query |= condition

    query_set = query_set.filter(query)
    return query_set

def _search_by_condition(query_set, conditions):
    '''
    :param query_set:
    :param conditions: {
        'categorieis':[category_id, category_id, ...],
        'areas':[
            {
                'province_id': province_id,
                'city_id': city_id,
                'area_id': area_id,
                'station_id': station_id
            },
            ...
        ]
    }
    :return:
    '''
    categories = conditions['categories']
    query_set = _search_by_categories(query_set, categories)

    areas = conditions['areas']
    query_set = _search_by_areas(query_set, areas)
    return query_set

def search_questions(query_set, limit, offset, search_text, search_condition, sort_type, distinct=False):
    if search_text:
        query_set = query_set.filter(Q(title__icontains=search_text) | Q(body__icontains=search_text))

    if search_condition:
        query_set = _search_by_condition(query_set, search_condition)

    if distinct:
        query_set = query_set.distinct()

    if sort_type == settings.SEARCH_POPULAR_TYPE:
        query_set = query_set.order_by('-point')
    elif sort_type == settings.SEARCH_RELATION_TYPE:
        query_set = query_set.order_by('-created_at')
    else:
        query_set = query_set.order_by('-created_at')

    total_length = query_set.count()
    query_set = query_set[offset:offset + limit]
    return query_set, total_length