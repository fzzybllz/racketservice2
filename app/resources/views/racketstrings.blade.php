
@extends('layouts.default')

@section('content')
<h2 class="mt-5">Alle Saiten</h2>
    
    <table class="table mt-5">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Hersteller</th>
        <th scope="col">Modell</th>
        <th scope="col">Stärke</th>
        <th scope="col">Länge</th>
        <th scope="col">Farbe</th>
        <th scope="col">Typ</th>
        <th scope="col">Genutzt</th>
        <th scope="col">Verfügbar</th>
        <th scope="col">Angelegt</th>
        <th scope="col">Aktionen</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($racketstrings as $racketstring)
        <tr>
            <td> {{ $racketstring->id }} </td>
            <td> {{ $racketstring->manufacturer }} </td>
            <td> {{ $racketstring->model }} </td>
            <td> {{ $racketstring->strength }} mm</td>
            <td> {{ $racketstring->length }} m</td>
            <td> {{ $racketstring->color }} </td>
            <td> {{ $racketstring->type }} </td>
            <td> {{ $racketstring->times_used }} x</td>
            <td> {{ floor(($racketstring->length/12) - $racketstring->times_used) }} Stk.</td>
            <td> {{ $racketstring->created_at->format('d.m.Y') }} </td>
            <td>
                <form action="/delete/racketstring" method="post" onsubmit="return confirm('Die Besaitungsrolle mit dazugehörigen Aufträgen wirklich löschen?');">
                    @csrf
                    <input class="form-control" type="hidden" name="id" value="{{ $racketstring->id }}">
                    <button class="btn btn-primary" type="submit">Löschen</button>
                </form>
            </td>
            </tr>
        @endforeach
    </tbody>
    </table>

    {{ $racketstrings->render() }}
    
    <h2 class="mt-5">Saite hinzufügen</h2>

    <form class="mt-5" method="POST" action="/create/racketstring">
    <div class="form-group">
        @csrf
        <label for="manufacturer">Hersteller*</label>
        <input class="form-control" required="required" type="text" name="manufacturer">
        <label for="model">Modell*</label>
        <input class="form-control" required="required" type="text" name="model">
        <label for="strength">Stärke*</label>
        <input class="form-control" required="required" type="text" name="strength">
        <label for="length">Länge*</label>
        <input class="form-control" required="required" type="number" name="length">
        <label for="color">Farbe</label>
        <input class="form-control" type="text" name="color">
        <label for="type">Typ</label>
        <input class="form-control" type="text" name="type">

        <button type="submit" class="btn btn-primary mt-2">Speichern</button>
    </div>
    </form>
@stop