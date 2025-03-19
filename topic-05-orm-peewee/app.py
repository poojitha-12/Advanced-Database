from flask import Flask, render_template, request, redirect, url_for
from database import db, Kind, Pet, initialize

app = Flask(__name__)

# Initialize the database
initialize('pets.db')

@app.route('/')
def index():
    pets = Pet.select().join(Kind)
    kinds = Kind.select()
    return render_template('index.html', pets=pets, kinds=kinds)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        owner = request.form['owner']
        kind_name = request.form['kind_name']  # Get the kind name from the form

        # Check if the kind already exists in the database
        kind = Kind.get_or_none(Kind.kind_name == kind_name)
        if not kind:
            # If the kind doesn't exist, create a new kind
            kind = Kind(kind_name=kind_name, food="Unknown", noise="Unknown")
            kind.save()

        # Create the pet
        pet = Pet(name=name, age=age, owner=owner, kind=kind)
        pet.save()
        return redirect(url_for('index'))

    return render_template('add_pet.html')

@app.route('/add_kind', methods=['GET', 'POST'])
def add_kind():
    if request.method == 'POST':
        kind_name = request.form['kind_name']
        food = request.form['food']
        noise = request.form['noise']

        kind = Kind(kind_name=kind_name, food=food, noise=noise)
        kind.save()
        return redirect(url_for('index'))
    return render_template('add_kind.html')

@app.route('/pet/<int:pet_id>')
def pet_detail(pet_id):
    pet = Pet.get_or_none(Pet.id == pet_id)
    if pet:
        return render_template('pet_detail.html', pet=pet)
    return "Pet not found", 404

@app.route('/kind/<int:kind_id>')
def kind_detail(kind_id):
    kind = Kind.get_or_none(Kind.id == kind_id)
    if kind:
        pets = Pet.select().where(Pet.kind == kind)
        return render_template('kind_detail.html', kind=kind, pets=pets)
    return "Kind not found", 404

@app.route('/pet/update/<int:pet_id>', methods=['GET', 'POST'])
def update_pet(pet_id):
    pet = Pet.get_or_none(Pet.id == pet_id)
    if not pet:
        return "Pet not found", 404

    if request.method == 'POST':
        pet.name = request.form['name']
        pet.age = int(request.form['age'])
        pet.owner = request.form['owner']
        kind_id = int(request.form['kind_id'])

        kind = Kind.get_or_none(Kind.id == kind_id)
        if kind:
            pet.kind = kind
            pet.save()
            return redirect(url_for('index'))

    kinds = Kind.select()
    return render_template('update_pet.html', pet=pet, kinds=kinds)

@app.route('/pet/delete/<int:pet_id>')
def delete_pet(pet_id):
    pet = Pet.get_or_none(Pet.id == pet_id)
    if pet:
        pet.delete_instance()
    return redirect(url_for('index'))

@app.route('/kind/update/<int:kind_id>', methods=['GET', 'POST'])
def update_kind(kind_id):
    kind = Kind.get_or_none(Kind.id == kind_id)
    if not kind:
        return "Kind not found", 404

    if request.method == 'POST':
        kind.kind_name = request.form['kind_name']
        kind.food = request.form['food']
        kind.noise = request.form['noise']
        kind.save()
        return redirect(url_for('index'))

    return render_template('update_kind.html', kind=kind)

@app.route('/kind/delete/<int:kind_id>')
def delete_kind(kind_id):
    kind = Kind.get_or_none(Kind.id == kind_id)
    if kind:
        kind.delete_instance()
    return redirect(url_for('index'))

@app.route('/kind_list')
def kind_list():
    kinds = Kind.select()
    return render_template('kind_list.html', kinds=kinds)

if __name__ == '__main__':
    app.run(debug=True)