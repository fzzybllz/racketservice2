<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddHybridAndChangeOrderTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('order', function (Blueprint $table)
        {
            $table->decimal('main_strength', 3, 1)->change();
            $table->decimal('cross_strength', 3, 1)->change();
            $table->boolean('hybrid')->default('false')->after('racket_id');
            $table->integer('racketstring_cross_id')->unsigned()->nullable()->after('racketstring_id');
            $table->foreign('racketstring_cross_id')->references('id')->on('racketstring')->onDelete('cascade');

        });

    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('order', function (Blueprint $table)
        {
            $table->float('main_strength')->change();
            $table->float('cross_strength')->change();
            $table->dropForeign('order_racketstring_cross_id_foreign');
            $table->dropColumn('racketstring_cross_id');
            $table->dropColumn('hybrid');
        });
    }
}
