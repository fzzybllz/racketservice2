<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Racket extends Model
{
    protected $table = 'racket';

    public function owner()
    {
        return $this->belongsTo('App\Customer', 'customer_id', 'id');
    }
}
