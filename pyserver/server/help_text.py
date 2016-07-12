def getHelpPageBody():
    '''
    self documentation, based on 
    https://github.com/christiana/blackbook/wiki/REST-API-specification
    '''
    return '''

<body>
<h1>Black Book REST API</h1>
<p>
</p>

<h2>Methods</h2>
<table border=\"1\">
<tr>
    <th>method</th>
    <th>resource</th>
    <th>description</th>
    <th>input arguments</th>
    <th>return arguments</th>
</tr>

<tr>
    <td>GET</td>
    <td>/</td>
    <td>return help page</td>
    <td></td>
    <td>text/html</td>
</tr>
<tr style="border-bottom:1px solid black"><td colspan="100%"></td></tr>

<tr>
    <td>GET</td>
    <td>/trips</td>
    <td>Get list of trips</td>
    <td></td>
    <td>application/json list of id:string</td>
</tr>
<tr>
    <td>POST</td>
    <td>/trips</td>
    <td>Generate new trip</td>
    <td>trip_object<br>(containing suggested trip_id)</td>
    <td>application/json trip_id:string</td>
</tr>
<tr>
    <td>GET</td>
    <td>/trips/{trip}</td>
    <td>Get trip info</td>
    <td></td>
    <td>trip_object</td>
</tr>
<tr>
    <td>PUT</td>
    <td>/trips/{trip}</td>
    <td>Update trip</td>
    <td>trip_object</td>
    <td></td>
</tr>
<tr>
    <td>DELETE</td>
    <td>/trips/{trip}</td>
    <td>Remove trip</td>
    <td></td>
    <td></td>
</tr>
<tr style="border-bottom:1px solid black"><td colspan="100%"></td></tr>

<tr>
    <td>GET</td>
    <td>/trips/{trip}/persons</td>
    <td>Get list of persons</td>
    <td></td>
    <td>application/json list of id:string</td>
</tr>
<tr>
    <td>POST</td>
    <td>/trips/{trip}/persons</td>
    <td>add a person</td>
    <td>person_object<br>(fails if id already exist)</td>
    <td></td>
</tr>
<tr>
    <td>GET</td>
    <td>/trips/{trip}/persons/{person}</td>
    <td>Get person</td>
    <td></td>
    <td>person_object</td>
</tr>
<tr>
    <td>PUT</td>
    <td>/trips/{trip}/persons/{person}</td>
    <td>Update person</td>
    <td>person_object</td>
    <td></td>
</tr>
<tr>
    <td>DELETE</td>
    <td>/trips/{trip}/persons/{person}</td>
    <td>Remove person</td>
    <td></td>
    <td></td>
</tr>
<tr style="border-bottom:1px solid black"><td colspan="100%"></td></tr>

<tr>
    <td>GET</td>
    <td>/trips/{trip}/payments</td>
    <td>Get list of payments ids</td>
    <td></td>
    <td>application/json list of id:string</td>
</tr>
<tr>
    <td>POST</td>
    <td>/trips/{trip}/payments</td>
    <td>New payment</td>
    <td>payment_object<br>(fails if id already exist). Use id="" to request a new id</td>
    <td>application/json id:string</td>
</tr>
<tr>
    <td>GET</td>
    <td>/trips/{trip}/payments/{payment}</td>
    <td>Get payment</td>
    <td></td>
    <td>payment_object</td>
</tr>
<tr>
    <td>PUT</td>
    <td>/trips/{trip}/payments/{payment}</td>
    <td>Update payment</td>
    <td>payment_object</td>
    <td></td>
</tr>
<tr>
    <td>DELETE</td>
    <td>/trips/{trip}/payments/{payment}</td>
    <td>Remove payment</td>
    <td></td>
    <td></td>
</tr>
<tr style="border-bottom:1px solid black"><td colspan="100%"></td></tr>

<tr>
    <td>VARIES</td>
    <td>/trips/{trip}/debts/{debt}</td>
    <td>Debts, collection of methods similar to payment.</td>
    <td></td>
    <td></td>
</tr>
<tr style="border-bottom:1px solid black"><td colspan="100%"></td></tr>

</table>








<h2>Objects</h2>
<table border=\"1\">
<tr>
    <th>object</th>
    <th>description</th>
    <th>contents</th>
</tr>

<tr>
    <td>trip_object</td>
    <td>One trip</td>
    <td>id:string,<br> name:string,<br> date:iso_date,<br> description:string</td>
</tr>
<tr>
    <td>person_object</td>
    <td>One person in the context of a trip. Name, weight (how much of the total should be paid by the person), balance (how much should the person pay or get back).</td>
    <td>application/json: 
        id:string,<br>
        name:string,<br>
        weight:float,<br> 
        balance:float,readonly.</td>
</tr>
<tr>
    <td>payment_object</td>
    <td>One payment made by one person (creditor) on behalf of a subset of the others (participants).</td>
    <td>application/json:<br> 
        id:string,<br> 
        type:payment_type,<br> 
        creditor:string,<br> 
        amount:float,<br> 
        currency:currency_type,<br> 
        rate:rate_type,<br> 
        description:string,<br> 
        date:iso_date,<br> 
        participants:list_of_person_id.<br>
        No participants means all.</td>
</tr>
<tr>
    <td>payment_type</td>
    <td>Type of payment. <br>type=split: Amount should be split among all participants according to weight.<br>type=debt: participants owes the creditor the given amount. </td>
    <td>string, One of {split, debt}. </td>
</tr>
<tr>
    <td>currency_type</td>
    <td>The type of currency used in a payment.</td>
    <td>text, use standard acronyms (NOK, EUR, ...). Default is none.</td>
</tr>
<tr>
    <td>rate_type</td>
    <td>Exchange rate for the given currency, from payment currency to internal currency.</td>
    <td>Default is 1.</td>
</tr>
</table>


</body>
        '''
