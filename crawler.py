import requests
from lxml.html import soupparser

from Company import Company
import parse


def crawl_page(skip):
    """ Get urls and return companies from the page specified skip.
    """
    URL = "http://ccs.career.cornell.edu/CareerFair/CarFair_SearchCode.php?link=yes&Company_Name=*&skip=" + str(skip)
    r = requests.get(URL)
    html = r.text.encode('utf-8')
    soup = soupparser.fromstring(html)
    trs = soup.xpath("//table[@id='mytables']//table[1]/tr")[3:]
    companies = []
    for tr in trs:
        a = tr.xpath("td/a")[0]
        name, url = a.text, "http://ccs.career.cornell.edu/CareerFair/" + a.attrib['href']
        id = get_id(url)
        company = Company(id)
        company.name = name
        company.url = url
        company = parse_company(company, url)
        companies.append(company)
    return companies


def get_id(url):
    """ Get company id from url.
    """
    return url.split('?')[1].split('=')[1].split('&')[0]


def parse_company(company, url):
    """ Return a `Company` object from url.
    """
    r = requests.get(url)
    html = r.text.encode('utf-8')
    soup = soupparser.fromstring(html)
    trs = soup.xpath("//table[@id='mytables']//table[1]/tr")
    for idx, tr in enumerate(trs):
        key = tr.xpath("td[1]//text()")
        if key:
            if key[0] == 'Website':
                company.website = tr.xpath("td[2]/a")[0].attrib['href']
            elif key[0] == 'Industry':
                company.industry = tr.xpath("td[2]")[0].text
            elif key[0] == 'Overview':
                company.overview = tr.xpath("td[2]")[0].text
            elif key[0] == 'Days Attending':
                days = tr.xpath("td[2]//text()")[0]
                if '1' in days:
                    company.days = [1]
                elif '2' in days:
                    company.days = [2]
                else:
                    company.days = [1, 2]
            elif key[0] == 'Degree Level':
                for inp in tr.xpath("td/input"):
                    if inp.attrib.get('checked'):
                        degree_level = inp.attrib.get('name')
                        if degree_level == 'DegLev_BA':
                            company.degrees['bachelor'] = True
                        elif degree_level == 'DegLev_MA':
                            company.degrees['master'] = True
                        elif degree_level == 'DegLev_PH':
                            company.degrees['phd'] = True
            elif key[0] == 'Job Types':
                for inp in tr.xpath("td/input"):
                    if inp.attrib.get('checked'):
                        job_type = inp.attrib.get('name')
                        if job_type == 'JobType_FT':
                            company.job_types['full-time'] = True
                        elif job_type == 'JobType_PT':
                            company.job_types['part-time'] = True
                        elif job_type == 'JobType_IN':
                            company.job_types['internship'] = True
                        elif job_type == 'JobType_CO':
                            company.job_types['co-op'] = True
            elif 'Job Title' in key[0]:
                job_title = tr.xpath("td[2]//text()")[0]
                company.job_titles.append(job_title)
            elif key[0].startswith('Work Authorization'):
                for inp in tr.xpath("td/input") + trs[idx+1].xpath("td/input"):
                    if inp.attrib.get('checked'):
                        authorization = inp.attrib.get('name')
                        if authorization == 'WorkAuth_CI':
                            company.authorizations['citizen'] = True
                        elif authorization == 'WorkAuth_F1':
                            company.authorizations['f-1'] = True
                        elif authorization == 'WorkAuth_J1':
                            company.authorizations['j-1'] = True
                        elif authorization == 'WorkAuth_PR':
                            company.authorizations['citizen/perm'] = True
                        elif authorization == 'WorkAuth_H1':
                            company.authorizations['h1-b'] = True
                        elif authorization == 'WorkAuth_TN':
                            company.authorizations['tn'] = True
    return company


if __name__ == '__main__':
    with open('data.json', 'a') as f:
        f.seek(0)
        f.truncate()
        f.write('{\n\t"companies": [\n')
        for skip in xrange(0, 270, 10):
            cs = crawl_page(skip)
            print "crawl_page at %s completed." % str(skip)
            for c in cs:
                f.write('\t\t' + c.to_json() + ',\n')
        f.seek(-2, 2)
        f.truncate()
        f.write('\n\t]\n}')

        parse.parse()
