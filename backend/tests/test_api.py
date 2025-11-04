import httpx
from pathlib import Path
from logging import getLogger


logger = getLogger(__file__)


CURRENT_DIR = CONFIG_DIR = Path(__file__).resolve()

PASSENGER_ENDPOINT = 'http://localhost:8000/v1/passenger'


def test_upload_csv():
    upload_api = f'{PASSENGER_ENDPOINT}/upload-csv'
    dataset = CURRENT_DIR.parent / "titanic_dataset" / "train.csv"

    try:
        with open(dataset, 'rb') as f:
            response = httpx.post(upload_api, files={'file': f})
            # Check the response
            if response.status_code == 200:
                logger.info(f"OK response: {response.json()}", )
            else:
                logger.warning("Bad response:", response.text)
    except httpx.RequestError as e:
        logger.error(f"An error occurred during the API request: {e}")


def test_get_passengers():
    get_passengers_api = f'{PASSENGER_ENDPOINT}/all'
    resp = httpx.get(get_passengers_api)
    logger.info(resp)


if __name__ == "__main__":
    test_get_passengers()



# TODO:
# test API Ingestion
# validate the following names
# 102	1	3	Mr	"Pentcho"		Petroff
# 147	1	3	Mr	"Wennerstrom"		Andersson
# 149	1	2	Mr	"Louis M	Hoffman"	Navratil
# 162	1	2	Mrs	Elizabeth "Bessie" Inglis	Milne	Watt
# 188	1	1	Mr	"Mr C	Rolmane"	Romaine
# 200	1	2	Miss	"Mrs	Harbeck"	Yrois
# 228	1	3	Mr	"Henry"		Lovell
# 382	1	3	Miss	"Mary"		Nakid
# 428	1	2	Miss	"Mrs Kate Louise Phillips	Marshall"	Phillips
# 508	1	1	Mr	"George Arthur	Brayton"	Bradley
# 519	1	2	Mrs	Florence "Mary" Agnes	Hughes	Angle
# 554	1	3	Mr	"Philip	Zenni"	Leeni
# 573	1	1	Mr	"Irving"		Flynn
# 600	1	1	Sir	"Mr	Morgan"	Duff Gordon
# 605	1	1	Mr	"Mr E	Haven"	Homer
# 706	1	2	Mr	"Mr Henry	Marshall"	Morley
# 710	1	3	Master	"William	George"	Moubarek
# 711	1	1	Mlle	"Mrs de	Villiers"	Mayne
