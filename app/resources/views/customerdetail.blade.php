@extends('layouts.default')

@section('content')
    <h2 class="mt-5">{{ $customer->firstname }} {{ $customer->surname }}</h2>
    
    <table class="table mt-5">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Nachname</th>
            <th scope="col">Vorname</th>
            <th scope="col">Adresse</th>
            <th scope="col">PLZ</th>
            <th scope="col">Ort</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td> {{ $customer->id }} </td>
            <td> {{ $customer->surname }} </td>
            <td> {{ $customer->firstname }} </td>
            <td> {{ $customer->adress }} </td>
            <td> {{ $customer->plz }} </td>
            <td> {{ $customer->place }} </td>
    </tbody>
    </table>

    <h2 class="mt-5">Schläger</h2>

    <table class="table mt-5">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Besitzer</th>
        <th scope="col">Hersteller</th>
        <th scope="col">Modell</th>
        <th scope="col">Muster</th>
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
            <td>
            </td>
            </tr>
        @endforeach
    </tbody>
    </table>
{{ $rackets->render() }}
@stop