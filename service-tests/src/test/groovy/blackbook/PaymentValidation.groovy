package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Unroll

class PaymentValidation extends Specification {
    def static client = new RESTClient('http://localhost:27222')
    def static sharedTripId

    def setupSpec() {
        client.setContentType('application/json')
        def response = client.post path: '/trips',
                body: [
                        name       : "Auto: PaymentValidation test",
                        date       : "2016-07-12",
                        description: "Uses for service test"
                ]
        sharedTripId = response.data.id
    }

    def cleanupSpec() {
        client.delete path: "/trips/$sharedTripId"
    }

    @Unroll
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when type is invalid"() {
        when:
          client.post path: "/trips/$tripId/payments",
                  body: [
                          type: 'invalid'
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when amount is not a number"() {
        when:
          client.post path: "/trips/$tripId/payments",
                  body: [
                          amount: 'femti'
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when creditor does not exist"() {
        when:
          client.post path: "/trips/$tripId/payments",
                  body: [
                          creditor: 'idonotexist',
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when rate is not a number"() {
        when:
          client.post path: "/trips/$tripId/payments",
                  body: [
                          rate: 'notanumber',
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when date is not a valid ISO date"() {
        when:
          client.post path: "/trips/$tripId/payments",
                  body: [
                          date: '15.07.2016',
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "POST /trips/#tripId/payments returns 400 BAD REQUEST when participants is not a list"() {
        when:
          client.post path: "/trips/$tripId/payments",
                  body: [
                          participants: '',
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

}