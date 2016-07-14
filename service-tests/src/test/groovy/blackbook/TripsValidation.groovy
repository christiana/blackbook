package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Specification


class TripsValidation extends Specification {
    def client = new RESTClient('http://localhost:27222')

    def setup() {
        client.contentType = 'application/json'
    }

    def "POST /trips returns 400 BAD REQUEST when date is invalid"() {
        when:
          client.post path: '/trips',
                  body: [
                          date: "12/07/2016",
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

    }

    def "PUT /trips returns 400 BAD REQUEST when date is invalid"() {
        when:
          client.put path: '/trips',
                  body: [
                          date: "12/07/2016",
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

    }

}