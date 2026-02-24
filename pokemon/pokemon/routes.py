from flask import Blueprint, render_template, request, redirect, url_for, flash
from pokemon.extensions import db
from pokemon.models import Pokemon, Type, User
from flask_login import login_required, current_user

pokemon_bp = Blueprint('pokemon', __name__, template_folder='templates')

@pokemon_bp.route('/')
@login_required
def index():
  query = db.select(Pokemon).where(Pokemon.user_id == current_user.id)
  pokemons = db.session.scalars(query).all()
  return render_template('pokemon/index.html', 
                         title='Pokemon Page',
                         pokemons=pokemons)

@pokemon_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_pokemon():
  query = db.select(Type)
  pokemon_types = db.session.scalars(query).all()
  if request.method == 'POST':
    name = request.form.get('name')
    height = request.form.get('height')
    weight = request.form.get('weight')
    description = request.form.get('description')
    img_url = request.form.get('img_url')
    user_id = current_user.id
    types = request.form.getlist('pokemon_types')
    
    p_types = []
    for id in types:
      p_types.append(db.session.get(Type, id))
     
    query = db.select(Pokemon).where(Pokemon.name == name) 
    pokemon = db.session.scalars(query).all()
    if pokemon:
      flash(f'Pokemon {name} is already exist', 'warning')
      return redirect(url_for('pokemon.new_pokemon'))
    new_pokemon = Pokemon(
      name=name,
      height=height,
      weight=weight,
      description=description,
      img_url=img_url,
      user_id=user_id,
      types=p_types
    )
    db.session.add(new_pokemon)
    db.session.commit()
    flash(f'Add new Pokemon {name} successfully!', 'success')
    return redirect(url_for('pokemon.index'))

  return render_template('pokemon/new_pokemon.html', 
                         title='New Pokemon Page',
                         pokemon_types=pokemon_types)
