
@extends('layouts.default')

@section('content')
    <h2 class="mt-5">Alle Kunden</h2>
    
    <table class="table mt-5">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Nachname</th>
            <th scope="col">Vorname</th>
            <th scope="col">Adresse</th>
            <th scope="col">PLZ</th>
            <th scope="col">Ort</th>
            <th scope="col">Aktionen</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($customers as $customer)
        <tr>
            <td> 
                <a href="/customers/{{ $customer->id }}">
                {{ $customer->id }} </td>
                </a>
            <td> {{ $customer->surname }} </td>
            <td> {{ $customer->firstname }} </td>
            <td> {{ $customer->adress }} </td>
            <td> {{ $customer->plz }} </td>
            <td> {{ $customer->place }} </td>
            <td>
                <form action="/delete/customer" method="post" onsubmit="return confirm('Den Kunden mit dazugehörigen Aufträgen und Schlägern wirklich löschen?');">
                    @csrf
                    <input class="form-control" type="hidden" name="id" value="{{ $customer->id }}">
                    <button class="btn btn-primary" type="submit">Löschen</button>
                </form>
            </td>
            </tr>
        @endforeach
    </tbody>
    </table>

    {{ $customers->render() }}
    
    <h2 class="mt-5">Kunde hinzufügen</h2>

    <form class="mt-5" method="POST" action="/create/customer">
    <div class="form-group">
        @csrf
        <div class="form-row">
            <div class="col">
            <label for="firstname">Vorname*</label>
            <input class="form-control" required="required" type="text" name="firstname">
            </div>
            <div class="col">
            <label for="surname">Nachname*</label>
            <input class="form-control" required="required" type="text" name="surname">
            </div>
        </div>
        <label for="adress">Adresse</label>
        <input class="form-control" type="text" name="adress">
        <div class="form-row">
            <div class="form-group col-md-4">
            <label for="plz">PLZ</label>
            <input class="form-control" type="text" name="plz">
            </div>
            <div class="form-group col-md-8">
            <label for="place">Ort</label>
            <input class="form-control" type="text" name="place">
            </div>
        </div>
        <button type="submit" class="btn btn-primary mt-2">Speichern</button>
    </div>
    </form>
@stop