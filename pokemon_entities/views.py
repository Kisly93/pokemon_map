import folium



from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    datetime_now = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entity = PokemonEntity.objects.filter(appeared_at__lte=datetime_now, disappeared_at__gt=datetime_now)
    for pokemon_entity in pokemon_entity:
        img_url = request.build_absolute_uri(location=pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = request.build_absolute_uri(location=pokemon.image.url)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    datetime_now = localtime()
    pokemon_entity = PokemonEntity.objects.filter(appeared_at__lte=datetime_now, disappeared_at__gt=datetime_now)
    for pokemon_entity in pokemon_entity:
        img_url = request.build_absolute_uri(location=pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )
    pokemon_data = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': pokemon.image.url,
        'description': pokemon.description,
    }
    if pokemon.parent:
        parent_data = {
            'title_ru': pokemon.parent.title,
            'pokemon_id': pokemon.parent.id,
            'img_url': request.build_absolute_uri(location=pokemon.parent.image.url)
        }
        pokemon_data['previous_evolution'] = parent_data
    kids = pokemon.kids.all()
    if kids:
        kid_data = {
            'title_ru': kids[0].title,
            'pokemon_id': kids[0].id,
            'img_url': request.build_absolute_uri(location=kids[0].image.url)
        }
        pokemon_data['next_evolution'] = kid_data
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
