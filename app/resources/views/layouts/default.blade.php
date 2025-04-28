<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <title>Racket Service</title>

        <!-- Fonts -->
        <link href="https://fonts.googleapis.com/css?family=Nunito:200,600" rel="stylesheet">

        <!-- Styles -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        
    <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">RacketService</a>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <a class="nav-link" href="/customers">Kunden</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/racketstrings">Saiten</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/rackets">Schläger</a>
                </li>

            </ul>
            <span class="">v0.1</span>
        </div>
    </nav>

    @if (session('error'))
        <div class="container mt-5">
            <div class="alert alert-error">
                {{ session('error') }}
            </div>
        </div>
    @endif
    @if (session('alert'))
        <div class="container mt-5">
            <div class="alert alert-success">
                {{ session('alert') }}
            </div>
        </div>
    @endif
    <div class="container">
        @yield('content')
    </div>
    </body>
</html>