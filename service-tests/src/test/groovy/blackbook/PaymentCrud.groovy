package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Ignore
import spock.lang.Specification
import spock.lang.Stepwise
import spock.lang.Unroll

@Stepwise
class PaymentCrud extends Specification {

    def static client = new RESTClient('http://localhost:27222')
    def static sharedTripId
    def static sharedPaymentId

    def setupSpec() {
        client.setContentType('application/json')
        def response = client.post path: '/trips',
                body: [
                        name       : "Auto: PaymentCrud test trip",
                        date       : "2016-07-12",
                        description: "Uses for service test"
                ]
        sharedTripId = response.data.id
    }

    def cleanupSpec() {
        client.delete path: "/trips/$sharedTripId"
    }

    @Unroll
    def "GET /trips/#tripId/payments returns status 200"() {
        when:
          def response = client.get path: "/trips/$tripId/payments"

        then:
          response.status == 200

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "GET /trips/#tripId/payments returns an empty list when no payments has been added"() {
        when:
          def response = client.get path: "/trips/$tripId/payments"

        then:
          response.data instanceof List
          response.data.size() == 0

        where:
          tripId << [sharedTripId]

    }

    @Unroll
    def "GET /trips/#tripId/payments/#personId returns 404 NOT FOUND when trip does not exist "() {
        when:
          client.get path: "/trips/$tripId/payments/$personId"

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404

        where:
          tripId << [sharedTripId]
          personId << ['1']

    }


    @Unroll
    def "POST /trips/#tripId/payments returns 201 CREATED and response contains created object id"() {
        when:
          def response = client.post path: "/trips/$tripId/payments",
                  body: [
                          type        : 'split',
                          creditor    : '',
                          amount      : 10,
                          currency    : 'NOK',
                          rate        : 1,
                          description : 'Ham',
                          date        : "2016-07-12",
                          participants: '',
                  ]

          sharedPaymentId = response.data.id

        then:
          sharedPaymentId
          response.status == 201

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    @Ignore
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when type is invalid"() {
        when:
          def response = client.post path: "/trips/$tripId/payments",
                  body: [
                          type        : 'invalid',
                          creditor    : '',
                          amount      : 10,
                          currency    : 'NOK',
                          rate        : 1,
                          description : 'Ham',
                          date        : "2016-07-12",
                          participants: '',
                  ]

          sharedPaymentId = response.data.id

        then:
          sharedPaymentId
          response.status == 400

        where:
          tripId << [sharedTripId]
    }


    @Unroll
    def "GET /trips/#tripId/payments/#personId returns person object"() {
        when:

          def response = client.get path: "/trips/$tripId/payments/$personId"

        then:
          response.status == 200
          response.data.type == 'split'
          response.data.creditor == ''
          response.data.amount == 10
          response.data.currency == 'NOK'
          response.data.rate == 1
          response.data.description == 'Ham'
          response.data.date == '2016-07-12'
          response.data.participants == ''


        where:
          tripId       | personId
          sharedTripId | sharedPaymentId

    }

    @Unroll
    def "GET /trips/#tripId/payments returns a list with one person when one person has been added"() {
        when:
          def response = client.get path: "/trips/$tripId/payments"

        then:
          response.data.size() == 1
          response.data.first() == sharedPaymentId

        where:
          tripId       | personId
          sharedTripId | sharedPaymentId

    }

    @Unroll
    def "PUT /trips/#tripId/payments/#personId returns 404 NOT FOUND when the person does not exist"() {
        when:
          client.put path: "/trips/$tripId/payments/$personId",
                  body: [
                          name  : "Reidar Reisgutt",
                          weight: 0.9
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404


        where:
          tripId       | personId
          sharedTripId | 'does_not_exist'

    }

    @Unroll
    def "PUT /trips/#tripId/payments/#personId returns 202 ACCEPTED when the trip exists"() {
        when:
          def response = client.put path: "/trips/$tripId/payments/$personId",
                  body: [
                          name       : "Første tur",
                          date       : "2016-07-12",
                          description: "En kjip tur til Ålborg"
                  ]

        then:
          response.status == 202

        where:
          tripId       | personId
          sharedTripId | sharedPaymentId

    }

    @Unroll
    def "DELETE /trips/#tripId/payments/#personId returns 404 NOT FOUND when trip does not exist"() {
        when:
          client.delete path: "/trips/#tripId/payments/#personId"

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404

        where:
          tripId       | personId
          sharedTripId | 'does_not_exist'

    }

    @Unroll
    def "DELETE /trips/#tripId/payments/#personId returns 202 ACCEPTED when trip exists"() {
        when:
          def response = client.delete path: "/trips/$tripId/payments/$personId"

        then:
          response.status == 202

        where:
          tripId       | personId
          sharedTripId | sharedPaymentId
    }

}