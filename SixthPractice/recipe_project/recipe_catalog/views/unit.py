from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipe_catalog.models import Unit
from recipe_catalog.forms import UnitForm
from recipe_catalog.constants import templates

@login_required
def manage_units(request):
    user_units = Unit.objects.filter(author=request.user)
    return render(request, templates['manage_units_page'], {
        'units': user_units
    })

@login_required
def add_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Unit.objects.filter(name=name, author=request.user).exists():
                form.add_error('name', 'Единица измерения с таким названием уже существует.')
                messages.error(request, 'Ошибка: единица измерения с таким названием уже существует.')
            else:
                unit = form.save(commit=False)
                unit.author = request.user
                unit.save()
                messages.success(request, 'Единица измерения успешно добавлена.')
                return redirect('manage-units')
        else:
            messages.error(request, 'Ошибка при добавлении единицы измерения.')
    else:
        form = UnitForm()

    return render(request, templates['add_units_page'], {'form': form})

@login_required
def edit_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk, author=request.user)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Единица измерения успешно обновлена.')
            return redirect('manage-units')
        else:
            messages.error(request, 'Ошибка при редактировании единицы измерения.')
    else:
        form = UnitForm(instance=unit)

    return render(request, templates['edit_units_page'], {'form': form, 'unit': unit})

@login_required
def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk, author=request.user)

    if request.method == 'POST':
        unit.delete()
        messages.success(request, 'Единица измерения успешно удалена.')
        return redirect('manage-units')

    return render(request, templates['delete_units_page'], {'unit': unit})