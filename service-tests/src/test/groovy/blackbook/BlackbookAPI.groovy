package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import net.sf.json.JSON
import spock.lang.Specification
import spock.lang.Stepwise


@Stepwise
class BlackbookAPI extends Specification {

    def client = new RESTClient('http://localhost:27222')

    def "GET /trips returns status 200"() {
        when:
          def resp = client.get path: '/trips'

        then:
          resp.status == 200
    }

    def "GET /trips returns application/json content-type"() {
        when:
          def resp = client.get path: '/trips'

        then:
          resp.contentType == 'application/json'

    }

    def "GET /trips returns an empty list"() {
        when:
          def resp = client.get path: '/trips'

        then:
          resp.data instanceof List
          resp.data.size() == 0

    }

    def "GET none existing trip returns 404 NOT FOUND"() {
        when:
          client.get path: '/trips/1'

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404
    }

    def "GET none existing trip returns application/json content-type"() {
        when:
          client.get path: '/trips/1'

        then:
          def ex = thrown(HttpResponseException)
          ex.response.contentType == 'application/json'
    }

}