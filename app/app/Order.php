<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Order extends Model
{
    protected $table = 'order';

    public function customer()
    {
        return $this->belongsTo('App\Customer', 'customer_id', 'id');
    }

    public function racket()
    {
        return $this->belongsTo('App\Racket', 'racket_id', 'id');
    }

    public function racketstring()
    {
        return $this->belongsTo('App\RacketString', 'racketstring_id', 'id');
    }

    
}
