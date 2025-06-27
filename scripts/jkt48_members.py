import csv
import os
import re
import json
import uuid
from bs4 import BeautifulSoup

def scrape_jkt48_members_from_html(filepath):
    """
    Mengambil data nama member dan link gambar profil dari file HTML lokal (jkt48.com),
    sesuai dengan struktur HTML JKT48 terbaru dan menangani spasi nama.
    """
    members_data = []
    
    # Memeriksa apakah file HTML ada
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' tidak ditemukan. Pastikan kamu sudah menyimpan halaman HTML.")
        return members_data

    try:
        # Membuka dan membaca konten file HTML
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Membuat objek BeautifulSoup untuk mengurai HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Mencari semua div dengan class 'entry-member'
        # Setiap div ini adalah container untuk informasi satu member
        member_entries = soup.find_all('div', class_='entry-member')

        print(f"Jumlah member yang ditemukan di {os.path.basename(filepath)}: {len(member_entries)}")

        if not member_entries:
            print(
                "Tidak ada elemen 'entry-member' yang ditemukan. Cek kembali struktur HTML website atau nama class."
            )
            # Ini bisa terjadi jika struktur HTML berubah lagi atau file yang disimpan tidak lengkap
            return members_data

        for entry in member_entries:
            # Mengambil tag <img> di dalam 'entry-member' untuk link gambar profil
            img_tag = entry.find('img')
            member_img_src = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'N/A'
            
            # Mengambil tag <p> dengan class 'entry-member__name' untuk nama member
            name_tag = entry.find('p', class_='entry-member__name')
            
            # Memproses nama member agar memiliki spasi yang benar
            if name_tag and name_tag.find('a'):
                # get_text(separator=' ', strip=True) akan menggabungkan teks
                # dan mengganti tag <br> dengan spasi, lalu membersihkan whitespace.
                # ' '.join(... .split()) akan menghilangkan spasi ganda dan merapikan string.
                member_name = ' '.join(name_tag.find('a').get_text(separator=' ', strip=True).split())
            else:
                member_name = 'N/A'

            # Memastikan URL gambar adalah absolut (dimulai dengan https://jkt48.com)
            if member_img_src and not member_img_src.startswith('http'):
                member_img_src = f"https://jkt48.com{member_img_src}"

            # Menambahkan data member ke list
            members_data.append({'Nama': member_name, 'Link Gambar Profil': member_img_src})

    except Exception as e:
        print(f"Terjadi error saat membaca atau menguraikan file HTML '{filepath}': {e}")
    return members_data

def scrape_jkt48_wikipedia_data(filepath):
    """
    Mengambil data detail member dari file HTML lokal Wikipedia, termasuk dari tabel member aktif dan trainee.
    """
    wiki_data = []
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' tidak ditemukan. Pastikan kamu sudah menyimpan halaman HTML.")
        return wiki_data

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        # Cari semua tabel yang mungkin berisi data member (baik member aktif maupun trainee)
        tables = soup.find_all('table', class_='wikitable')

        if not tables:
            print("Tabel member tidak ditemukan di file Wikipedia.")
            return wiki_data

        # Iterasi melalui setiap tabel yang ditemukan
        for table in tables:
            thead = table.find('thead')
            tbody = table.find('tbody')

            # Lewati tabel yang tidak memiliki struktur header dan body yang jelas (misalnya tabel pembungkus)
            if not thead or not tbody:
                continue

            # Ekstrak header dari tabel saat ini
            headers = []
            header_row = thead.find('tr')
            if not header_row:
                continue

            for th in header_row.find_all('th'):
                header_text = th.get_text(strip=True)
                # Membersihkan teks referensi seperti [14] dari header
                header_text = re.sub(r'\[\d+\]$', '', header_text)
                headers.append(header_text)

            # Jika tidak ada header, lanjut ke tabel berikutnya
            if not headers:
                continue

            # Ekstrak data baris member dari tabel saat ini
            for row in tbody.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == len(headers):
                    member_info = {}
                    for i, cell in enumerate(cells):
                        # Untuk kolom media sosial, pisahkan dengan baris baru untuk keterbacaan
                        if "media sosial" in headers[i].lower():
                            member_info[headers[i]] = cell.get_text(separator='\n', strip=True)
                        else:
                            member_info[headers[i]] = cell.get_text(strip=True)
                    # Hanya tambahkan jika ada data yang diekstrak
                    if member_info:
                        wiki_data.append(member_info)

        print(
            f"Jumlah total member (aktif + trainee) yang ditemukan di {os.path.basename(filepath)}: {len(wiki_data)}"
        )

    except Exception as e:
        print(f"Terjadi error saat membaca atau menguraikan file HTML '{filepath}': {e}")

    return wiki_data

def save_to_json(data, json_filepath):
    """
    Membersihkan, menerjemahkan kunci, memisahkan data kelahiran,
    dan menyimpan data langsung ke file JSON.
    """
    if not data:
        print("Tidak ada data untuk disimpan.")
        return

    KEY_MAPPING = {
        'Nama': 'name',
        'Link Gambar Profil': 'profile_picture_url',
        'Nama lengkap': 'full_name',
        'Nama panggilan': 'nickname',
        # 'Kelahiran (usia)' akan ditangani secara manual
        'Generasi': 'generation',
        'Salam perkenalan': 'introduction_phrase',
        'Mulai dan durasi bergabung (di JKT48)': 'join_details_jkt48',
        'Formasi sebelumnya (tanggal pembubaran atau terakhir bergabung)': 'previous_formation',
        'Mulai dan durasi bergabung (sebagai anggota tetap JKT48)': 'promoted_details_jkt48',
        'Sub-unit': 'sub_unit',
        'Nama fanbase': 'fanbase_name',
        'Ref.': 'reference',
    }

    try:
        # Pastikan direktori output ada jika diperlukan
        output_dir = os.path.dirname(json_filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        final_data = []
        for row in data:
            processed_row = {}
            # Tambahkan UUID unik untuk setiap record
            processed_row['id'] = str(uuid.uuid4())

            for indonesian_key, value in row.items():
                # Abaikan nilai-nilai yang tidak relevan
                if value in ('N/A', '', None):
                    continue

                if indonesian_key == 'Kelahiran (usia)':
                    # Membersihkan nilai dari referensi [..] dan usia (..)
                    # Contoh: "Jakarta,Indonesia, 26 Agustus 2006 (18 tahun)"
                    # Contoh: "Sydney,Australia, 23 Desember 2009 (15 tahun)[23]"
                    clean_value = re.sub(r'\[\d+\]', '', value).strip()
                    clean_value = re.sub(r'\s*\([^)]*tahun[^)]*\)\s*$', '', clean_value).strip()

                    last_comma_index = clean_value.rfind(',')
                    if last_comma_index != -1:
                        birth_place = clean_value[:last_comma_index].strip()
                        birth_date_raw = clean_value[last_comma_index + 1 :].strip()

                        # Membersihkan format tanggal ISO (YYYY-MM-DD) yang kadang muncul
                        birth_date = re.sub(r'^\s*\(\d{4}-\d{2}-\d{2}\)', '', birth_date_raw).strip()

                        processed_row['birth_place'] = birth_place
                        processed_row['birth_date'] = birth_date
                    else:
                        # Fallback jika format tidak terduga
                        processed_row['birth_details'] = value

                elif indonesian_key == 'Akun media sosial':
                    social_media_dict = {}
                    for line in value.split('\n'):
                        if ':' in line:
                            parts = line.split(':', 1)
                            sm_key = parts[0].strip().upper()
                            sm_value = parts[1].strip()
                            if sm_key == '@':
                                sm_key = 'THREADS'
                            elif sm_key == 'IDN':
                                sm_key = 'IDN_LIVE'
                            elif sm_key == 'IG':
                                sm_key = 'INSTAGRAM'
                            elif sm_key == 'SR':
                                sm_key = 'SHOWROOM'
                            elif sm_key == 'TT':
                                sm_key = 'TIKTOK'
                            social_media_dict[sm_key] = sm_value
                    if social_media_dict:
                        processed_row['social_media'] = social_media_dict
                else:
                    english_key = KEY_MAPPING.get(indonesian_key)
                    if english_key:
                        if english_key == 'nickname':
                            processed_row[english_key] = [
                                nick.strip() for nick in value.split(',') if nick.strip()
                            ]
                        else:
                            processed_row[english_key] = value

            if processed_row:
                final_data.append(processed_row)

        with open(json_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(final_data, json_file, indent=4, ensure_ascii=False)

        print(f"\nData berhasil disimpan langsung ke '{json_filepath}' dengan kunci Bahasa Inggris.")

    except Exception as e:
        print(f"Terjadi error saat menyimpan ke JSON: {e}")

if __name__ == "__main__":
    # --- PENTING: Langkah untuk Mendapatkan file HTML ---
    # 1. Buka browser dan kunjungi: https://jkt48.com/member/list?lang=id
    #    Simpan halaman sebagai "Webpage, Complete" dengan nama "jkt48_members.html"
    # 2. Buka browser dan kunjungi: https://id.wikipedia.org/wiki/Daftar_anggota_JKT48
    #    Simpan tabel "Anggota Aktif" sebagai file HTML dengan nama "jkt48_wikipedia.html"

    # Konfigurasi nama file input dan output
    html_jkt48_file = "jkt48_members.html"
    html_wikipedia_file = "jkt48_wikipedia.html"
    json_output_file = "jkt48_members.json"

    # 1. Ambil data dari Wikipedia (sumber utama)
    print(f"Memulai pengambilan data dari file HTML: '{html_wikipedia_file}'")
    wiki_data = scrape_jkt48_wikipedia_data(html_wikipedia_file)

    # 2. Ambil data dari jkt48.com (sumber gambar profil)
    print(f"\nMemulai pengambilan data dari file HTML: '{html_jkt48_file}'")
    members_data = scrape_jkt48_members_from_html(html_jkt48_file)

    # 3. Gabungkan data dengan logika yang lebih baik
    if wiki_data and members_data:
        print("\nMemulai proses penggabungan data...")
        jkt48_lookup = {member['Nama'].lower(): member for member in members_data}
        unmatched_jkt48_members = set(jkt48_lookup.keys())
        combined_data = []
        matches_found = 0

        for wiki_member in wiki_data:
            full_name_lower = wiki_member.get('Nama lengkap', '').lower()
            nicknames = [nick.strip().lower() for nick in wiki_member.get('Nama panggilan', '').split(',')]
            
            match_found_for_this_member = False
            
            # Strategi 1: Cocokkan nama dari jkt48.com dengan nama lengkap dari Wikipedia
            for jkt48_name_lower in list(unmatched_jkt48_members):
                # Memastikan semua kata dari nama pendek ada di nama panjang
                if set(jkt48_name_lower.split()) <= set(full_name_lower.split()):
                    match = jkt48_lookup[jkt48_name_lower]
                    
                    merged_record = wiki_member.copy()
                    merged_record.update(match)
                    combined_data.append(merged_record)
                    
                    unmatched_jkt48_members.remove(jkt48_name_lower)
                    match_found_for_this_member = True
                    matches_found += 1
                    break
            
            if match_found_for_this_member:
                continue

            # Strategi 2: Jika tidak ketemu, cocokkan dengan nama panggilan
            for jkt48_name_lower in list(unmatched_jkt48_members):
                if jkt48_name_lower in nicknames:
                    match = jkt48_lookup[jkt48_name_lower]
                    merged_record = wiki_member.copy()
                    merged_record.update(match)
                    combined_data.append(merged_record)
                    unmatched_jkt48_members.remove(jkt48_name_lower)
                    match_found_for_this_member = True
                    matches_found += 1
                    break
            
            # Jika tetap tidak ketemu, tambahkan saja data dari Wikipedia
            if not match_found_for_this_member:
                combined_data.append(wiki_member)
        
        # Tambahkan sisa member dari jkt48.com yang tidak ada di Wikipedia
        if unmatched_jkt48_members:
            print(f"\nPeringatan: {len(unmatched_jkt48_members)} member dari jkt48.com tidak dapat dicocokkan dengan data Wikipedia:")
            for name in sorted(list(unmatched_jkt48_members)):
                print(f" - {name.title()}")
                combined_data.append(jkt48_lookup[name])

        print(f"\nProses penggabungan selesai. {matches_found} data berhasil dicocokkan.")
        # 4. Simpan ke JSON
        save_to_json(combined_data, json_output_file)
    
    elif wiki_data:
        print("\nData dari jkt48.com tidak ditemukan. Hanya menyimpan data dari Wikipedia.")
        save_to_json(wiki_data, json_output_file)
    
    elif members_data:
        print("\nData dari Wikipedia tidak ditemukan. Hanya menyimpan data dari jkt48.com.")
        save_to_json(members_data, json_output_file)
    
    else:
        print("\nProses pengambilan data gagal atau tidak menemukan member sama sekali.")