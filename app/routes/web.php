<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', ['uses' => 'HomeController@orders']);
Route::get('/customers', ['uses' => 'HomeController@customers']);
Route::get('/customers/{id}', ['uses' => 'HomeController@customerdetail']);
Route::get('/rackets', ['uses' => 'HomeController@rackets']);
Route::get('/racketstrings', ['uses' => 'HomeController@racketstrings']);
Route::post('/create/{method}', ['uses' => 'HomeController@create']);
Route::post('/delete/{method}', ['uses' => 'HomeController@delete']);
Route::post('/update/{method}', ['uses' => 'HomeController@update']);

Auth::routes();