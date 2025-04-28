<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Exception;
use App\Racket;
use App\RacketString;
use App\Customer;
use App\Order;

class HomeController extends Controller
{
    public function rackets(Request $request) 
    {
        $rackets = Racket::paginate(10);
        $rackets->load('owner');
        $customers = Customer::all();
        return view('rackets', ['rackets' => $rackets, 'customers' => $customers]);
    }

    public function customers(Request $request) 
    {
        $customers = Customer::paginate(10);
        return view('customer', ['customers' => $customers]);
    }

    public function customerdetail(Request $request, $id)
    {
        $customer = Customer::find($id);
        $rackets = Racket::paginate(5);
        return view('customerdetail', ['customer' => $customer, 'rackets' => $rackets]);
    }

    public function racketstrings(Request $request) 
    {
        $racketStrings = RacketString::paginate(10);
        return view('racketstrings', ['racketstrings' => $racketStrings]);
    }

    public function orders(Request $request) 
    {
        $orders = Order::paginate(10);
        $orders->load(['racket', 'customer', 'racketstring']);

        $ordersOpen = Order::where('done', false)->get();
        $ordersOpen->load(['racket', 'customer', 'racketstring']);

        $customers = Customer::all();
        $customers->load('rackets');

        $customersJs = [];
        foreach($customers as $customer)
        {
            $customersJs[$customer->id] = $customer->rackets;
        }

        $customersJs = json_encode($customersJs);

        $racketstrings = RacketString::all();
        return view('order', 
                ['orders' => $orders,
                 'ordersOpen' => $ordersOpen,
                 'customers' => $customers,
                 'racketstrings' => $racketstrings,
                 'customersJs' => $customersJs]);
    }

    public function update(Request $request, $method)
    {
        switch($method)
        {
            case 'done':
                try
                {
                    $order = Order::find($request->id);
                    if($order && !$order->done)
                    {
                        $order->done = true;
                        $order->save();
                        return redirect('/')->with('alert', 'Auftrag abgeschlossen!');
                    }
                    return redirect('/');
                }
                catch(Exception $e)
                {
                    return redirect('/')->with('error', $e);
                }
                break;
        }
    }

    public function delete(Request $request, $method)
    {
        switch($method)
        {
            case 'racket':
                try
                {
                    $racket = Racket::find($request->id);
                    if($racket)
                    {
                        $racket->delete();
                        return redirect('/rackets')->with('alert', 'Schläger gelöscht');
                    }
                    return redirect('/rackets');
                }
                catch(Exception $e)
                {
                    return redirect('/rackets')->with('error', $e);
                }
                break;
            case 'order':
                try
                {
                    $order = Order::find($request->id);
                    if($order)
                    {
                        if(!$order->done)
                        {
                            $racketstring = RacketString::find($order->racketstring->id);
                            $racketstring->times_used = $racketstring->times_used - 1;
                            $racketstring->save();
                        }

                        $order->delete();
                        return redirect('/')->with('alert', 'Auftrag gelöscht');
                    }
                    return redirect('/');
                }
                catch(Exception $e)
                {
                    return redirect('/')->with('error', $e);
                }
                break;
            case 'racketstring':
                try
                {
                    $racketstring = RacketString::find($request->id);
                    if($racketstring)
                    {
                        $racketstring->delete();
                        return redirect('/racketstrings')->with('alert', 'Saite gelöscht');
                    }
                    return redirect('/racketstrings');
                }
                catch(Exception $e)
                {
                    return redirect('/racketstrings')->with('error', $e);
                }
                break;
            case 'customer':
                try
                {
                    $customer = Customer::find($request->id);
                    if($customer) {
                        $customer->delete();
                        return redirect('/customers')->with('alert', 'Kunde gelöscht');
                    }
                    
                    return redirect('/customers');
                }
                catch(Exception $e)
                {
                    return redirect('/customers')->with('error', $e);
                }
                break;
        }
    }

    public function create(Request $request, $method)
    {

        switch($method) 
        {
            case 'racket':
                try
                {
                    $racket = new Racket;
                    $racket->customer_id = $request->owner;
                    $racket->manufacturer = $request->manufacturer;
                    $racket->model = $request->model;
                    $racket->mains_skip = $request->mains_skip;
                    $racket->template = $request->template;
                    $racket->start2 = $request->start2;
                    $racket->start4 = $request->start4;
                    $racket->freetext = $request->freetext;
                    $racket->save();
                    return redirect('/rackets')->with('alert', 'Schläger gespeichert');
                }
                catch(Exception $e)
                {
                    return redirect('/rackets')->with('error', $e);
                }
                break;
            case 'racketstring':
                try
                {
                    $racketString = new RacketString();
                    $racketString->manufacturer = $request->manufacturer;
                    $racketString->model = $request->model;
                    $racketString->strength = $request->strength;
                    $racketString->length = $request->length;
                    $racketString->color = $request->color;
                    $racketString->type = $request->type;
                    $racketString->times_used = 0;
                    $racketString->save();
                    return redirect('/racketstrings')->with('alert', 'Saite gespeichert');
                }
                catch(Exception $e)
                {
                    return redirect('/racketstrings')->with('error', $e);
                }
                break;
            case 'customer':
                try
                {
                    $customer = new Customer;
                    $customer->surname = $request->surname;
                    $customer->firstname = $request->firstname;
                    $customer->adress = $request->adress;
                    $customer->plz = $request->plz;
                    $customer->place = $request->place;
                    $customer->save();
                    return redirect('/customers')->with('alert', 'Kunde gespeichert');
                }
                catch(Exception $e)
                {
                    return redirect('/customers')->with('error', $e);
                }
                break;
            case 'order':
                try
                {

                    $order = new Order;
                    $order->customer_id = $request->customer =="null"?null:$request->customer;
                    $order->racket_id = $request->racket =="Auswählen..."?null:$request->racket;
                    $order->hybrid = $request->hybrid;
                    $order->racketstring_id = $request->racketstring =="null"?null:$request->racketstring;
                    $order->racketstring_cross_id = $request->racketstring_cross =="null"?null:$request->racketstring_cross;
                    $order->main_strength = $request->main_strength;
                    $order->cross_strength = $request->cross_strength;
                    $order->done = false;
                    $order->save();

                    $racketstring = RacketString::find($order->racketstring->id);
                    if($racketstring)
                    {
                        $racketstring->times_used = $racketstring->times_used + 1;
                        $racketstring->save();
                    }
                    return redirect('/')->with('alert', 'Auftrag gespeichert');
                }
                catch(Exception $e)
                {
                    return redirect('/')->with('error', $e);
                }
                break;
            default:
                return redirect('/')->with('error', 'Bad method');
        }
    }
}
