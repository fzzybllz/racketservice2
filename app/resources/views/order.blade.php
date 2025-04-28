
@extends('layouts.default')

@section('content')
<h2 class="mt-5">Offene Aufträge</h2>
    
    <table class="table mt-5">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Kunde</th>
        <th scope="col">Schläger</th>
        <th scope="col">Besaitung</th>
        <th scope="col">Saitenstärke</th>
        <th scope="col">Anzugkraft Längs</th>
        <th scope="col">Anzugkraft Quer</th>
        <th scope="col">Erstellt</th>
        <th scope="col">Aktionen</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($ordersOpen as $order)
        <tr>
            <td> {{ $order->id }} </td>
            <td> {{ $order->customer->firstname }}, {{ $order->customer->surname }}</td>
            <td> {{ $order->racket->manufacturer }}, {{ $order->racket->model }} </td>
            <td> {{ $order->racketstring->manufacturer }}, {{ $order->racketstring->model }} #{{ $order->racketstring->id }}</td>
            <td> {{ $order->racketstring->strength }} mm</td>
            <td> {{ $order->main_strength }} kg</td>
            <td> {{ $order->cross_strength }} kg</td>
            <td> {{ $order->created_at->format('d.m.Y') }} </td>
            <td>
                <form action="/delete/order" method="post">
                    @csrf
                    <input class="form-control" type="hidden" name="id" value="{{ $order->id }}">
                    <button class="btn btn-primary" type="submit">Löschen</button>
                </form>
                <form action="/update/done" method="post">
                    @csrf
                    <input class="form-control" type="hidden" name="id" value="{{ $order->id }}">
                    <button class="btn btn-primary" type="submit">Done</button>
                </form>
            </td>
            </tr>
        @endforeach
    </tbody>
    </table>

    <h2 class="mt-5">Neuer Auftrag</h2>

    <form class="mt-5" method="POST" action="/create/order">
    <div class="form-group">
        @csrf
        <label for="customer">Kunde*</label>
        <select class="custom-select" required="required" name="customer" id="customerSelect">
            <option selected value="null">Auswählen...</option>
            @foreach ($customers as $customer)
                <option value="{{ $customer->id }}">{{ $customer->firstname }}, {{ $customer->surname }}</option>
            @endforeach
        </select>

        <label for="racket">Schläger*</label>
        <select class="custom-select" required="required" name="racket" id="racketSelect">
            <option selected>Zuerst Kunde wählen</option>
        </select>  

    <div class="form-row">
     <div class="form-group col-md-2">
        <label for="hybrid">Hybrid*</label>
        <select class="custom-select" name="hybrid" id="hybrid">
            <option selected value="false">Nein</option>
            <option value="true">Ja</option>
        </select>
     </div>
     <div class="form-group col-md-5">
        <label for="racketstring">Saite längs*</label>
        <select class="custom-select" required="required" name="racketstring" id="racketstringSelect">
            <option selected value="null">Auswählen...</option>
            @foreach ($racketstrings as $racketstring)
                @if((($racketstring->length/12) - $racketstring->times_used) >= 1)
                    <option value="{{ $racketstring->id }}">{{ $racketstring->manufacturer }}, {{ $racketstring->model }} #{{ $racketstring->id }}, noch ca. {{ floor(($racketstring->length/12) - $racketstring->times_used) }} Mal übrig</option>
                @endif
            @endforeach
        </select>
     </div>
     <div class="form-group col-md-5">
        <label for="racketstring">Saite quer</label>
        <select class="custom-select" name="racketstring_cross" id="racketstringcrossSelect">
            <option selected value="null">Auswählen...</option>
            @foreach ($racketstrings as $racketstring)
                @if((($racketstring->length/12) - $racketstring->times_used) >= 1)
                    <option value="{{ $racketstring->id }}">{{ $racketstring->manufacturer }}, {{ $racketstring->model }} #{{ $racketstring->id }}, noch ca. {{ floor(($racketstring->length/12) - $racketstring->times_used) }} Mal übrig</option>
                @endif
            @endforeach
        </select>
     </div>
    </div>

    <div class="form-row">
     <div class="col">    
        <label for="main_strength">Anzugkraft längs*</label>
        <input class="form-control" required="required" type="text" name="main_strength">
     </div>
     <div class="col">
        <label for="cross_strength">Anzugkraft quer*</label>
        <input class="form-control" required="required" type="text" name="cross_strength">
     </div>
    </div>
    <div class="form-group">
        <button type="submit" class="btn btn-primary mt-2">Speichern</button>
    </div>
    </form>

<h2 class="mt-5">Alle Aufträge</h2>
    
    <table class="table mt-5">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">Kunde</th>
        <th scope="col">Schläger</th>
        <th scope="col">Besaitung</th>
        <th scope="col">Saitenstärke</th>
        <th scope="col">Anzugkraft Längs</th>
        <th scope="col">Anzugkraft Quer</th>
        <th scope="col">Fertig</th>
        <th scope="col">Aktionen</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($orders as $order)
        <tr>
            <td> {{ $order->id }} </td>
            <td> {{ $order->customer->firstname }}, {{ $order->customer->surname }}</td>
            <td> {{ $order->racket->manufacturer }}, {{ $order->racket->model }}  #{{ $order->racket->id }} </td>
            <td> {{ $order->racketstring->manufacturer }}, {{ $order->racketstring->model }}</td>
            <td> {{ $order->racketstring->strength }} mm</td>
            <td> {{ $order->main_strength }} kg</td>
            <td> {{ $order->cross_strength }} kg</td>
            <td> {{ $order->updated_at->format('d.m.Y') }} </td>
            <td>
                <form action="/delete/order" method="post" onsubmit="return confirm('Den Auftrag wirklich löschen?');">
                    @csrf
                    <input class="form-control" type="hidden" name="id" value="{{ $order->id }}">
                    <button class="btn btn-primary" type="submit">Löschen</button>
                </form>
            </td>
            </tr>
        @endforeach
    </tbody>
    </table>

    {{ $orders->render() }}

    <script>
        var customers = JSON.parse('{!! $customersJs !!}');
        let customerSelect = document.querySelector('#customerSelect');
        let racketSelect = document.querySelector('#racketSelect');
        customerSelect.addEventListener('change', (e) => {
            let selectedCustomerId = e.target.value;
            if(selectedCustomerId != null) {
                racketSelect.innerHTML = '';
                let option = document.createElement('option');
                option.innerText = 'Auswählen...';
                racketSelect.appendChild(option);
                let selectedCustomer = customers[selectedCustomerId];
                selectedCustomer.forEach(item => {
                    let option = document.createElement('option');
                    option.value = item.id;
                    option.innerText = item.manufacturer+', '+item.model+' #'+item.id;
                    racketSelect.appendChild(option);
                });
            }
        });

    </script>
@stop