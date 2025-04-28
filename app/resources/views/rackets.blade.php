
@extends('layouts.default')

@section('content')
    
    <h2 class="mt-5">Alle Schläger</h2>
    
    <table class="table mt-5">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Besitzer</th>
        <th scope="col">Hersteller</th>
        <th scope="col">Modell</th>
        <th scope="col">Muster</th>
        <th scope="col">Mains-Skip</th>
        <th scope="col">Start2</th>
        <th scope="col">Start4</th>
        <th scope="col">Anmerkungen</th>
        <th scope="col">Aktionen</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($rackets as $racket)
        <tr>
            <td> {{ $racket->id }} </td>
            <td> {{ $racket->owner->firstname }}, {{ $racket->owner->surname }} </td>
            <td> {{ $racket->manufacturer }} </td>
            <td> {{ $racket->model }} </td>
            <td> {{ $racket->template }} </td>
            <td> {{ $racket->mains_skip }} </td>
            <td> {{ $racket->start2 }} </td>
            <td> {{ $racket->start4 }} </td>
            <td> {{ $racket->freetext }} </td>
            <td>
                <form action="/delete/racket" method="post" onsubmit="return confirm('Den Schläger von {{ $racket->owner->firstname }} {{ $racket->owner->surname }} wirklich löschen?');">
                    @csrf
                    <input class="form-control" type="hidden" name="id" value="{{ $racket->id }}">
                    <button class="btn btn-primary" type="submit">Löschen</button>
                </form>
            </td>
            </tr>
        @endforeach
    </tbody>
    </table>

    {{ $rackets->render() }}
    
    <h2 class="mt-5">Schläger hinzufügen</h2>

    <form class="mt-5" method="POST" action="/create/racket">
    <div class="form-group">
        @csrf
        <label for="owner">Besitzer</label>
        <select class="custom-select" name="owner" id="owenerSelect">
            <option selected>Auswählen...</option>
            @foreach ($customers as $customer)
                <option value="{{ $customer->id }}">{{ $customer->firstname }}, {{ $customer->surname }}</option>
            @endforeach
        </select>
        <label for="manufacturer">Hersteller*</label>
        <input class="form-control" required="required" type="text" name="manufacturer">
        <label for="model">Modell*</label>
        <input class="form-control" required="required" type="text" name="model">
        <label for="template">Muster</label>
        <input class="form-control" type="text" name="template">
        <label for="mains_skip">Mains-Skip</label>
        <input class="form-control" type="text" name="mains_skip">
        <label for="start2">Start2</label>
        <input class="form-control" type="text" name="start2">
        <label for="start4">Start4</label>
        <input class="form-control" type="text" name="start4">
        <label for="freetext">Anmerkungen</label>
        <textarea class="form-control" type="text" name="freetext"></textarea>

        <button type="submit" class="btn btn-primary mt-2">Speichern</button>
    </div>
    </form>
@stop