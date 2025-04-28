<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Customer extends Model
{
    protected $table = 'customer';

    public function rackets()
    {
        return $this->hasMany('App\Racket', 'customer_id', 'id');
    }
}
