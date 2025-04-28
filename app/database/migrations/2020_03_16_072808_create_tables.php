<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateTables extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('customer', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->string('surname');
            $table->string('firstname');
            $table->string('adress');
            $table->string('plz');
            $table->string('place');
        });
        Schema::create('racket', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->integer('customer_id');
            $table->foreign('customer_id')->references('id')->on('customer')->onDelete('cascade');
            $table->string('manufacturer');
            $table->string('model');
            $table->string('template')->nullable();
            $table->string('mains_skip')->nullable();
            $table->string('start2')->nullable();
            $table->string('start4')->nullable();
            $table->string('freetext')->nullable();
        });
        Schema::create('racketstring', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->string('manufacturer');
            $table->string('model');
            $table->text('strength');
            $table->float('length');
            $table->string('color')->nullable();
            $table->string('type')->nullable();
            $table->integer('times_used');
        });
        Schema::create('order', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->integer('customer_id');
            $table->foreign('customer_id')->references('id')->on('customer')->onDelete('cascade');
            $table->integer('racket_id');
            $table->foreign('racket_id')->references('id')->on('racket')->onDelete('cascade');
            $table->integer('racketstring_id');
            $table->foreign('racketstring_id')->references('id')->on('racketstring')->onDelete('cascade');
            $table->float('main_strength');
            $table->float('cross_strength');
            $table->boolean('done')->default('false');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('racket', function(Blueprint $table)
        {
            $table->dropForeign('racket_customer_id_foreign');
        });
        Schema::table('order', function(Blueprint $table)
        {
            $table->dropForeign('order_customer_id_foreign');
            $table->dropForeign('order_racket_id_foreign');
            $table->dropForeign('order_racketstring_id_foreign');
        });
        Schema::dropIfExists('racketstring');
        Schema::dropIfExists('racket');
        Schema::dropIfExists('customer');
        Schema::dropIfExists('order');
    }
}
