import os
from flask import Flask, jsonify, request
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    # Opening JSON file 
    x = {};
    filename = os.path.join(app.static_folder, 'data', 'appointment.json')
    

    with open(filename) as appointment:
        data = json.load(appointment)
        
        data['appointments'].sort(key = lambda x:x['date'])
        
    
    return json.dumps(data), 200

@app.route('/add', methods=['POST'])
def addAppointment():
    
    print(request.json)
    
    filename = os.path.join(app.static_folder, 'data', 'appointment.json')
    
    newdata = {};
     
    with open(filename) as json_file: 
        
        add = request.json['data']
        data = json.load(json_file)
        
        for check in data['appointments']:
            if(check['date']  == add['date']):
                if(add['time_in'] <= check['time_out'] and add['time_in'] >= check['time_in']):
                    return jsonify('Ttime error'), 400
                if(add['time_out'] <= check['time_out'] and add['time_out'] >= check['time_in']):
                    return jsonify('Ttime errorors'), 400
                    
        
        
        id = str(int(data['appointments'][-1]['id'])+1)
        add["id"]=id
        
        temp = data['appointments'] 
    
        temp.append(add) 
        
        newdata = {"appointments":temp}
    
    
    with open(filename,'w') as f: 
        json.dump(newdata, f, indent=4)
        
    return jsonify('Success'), 200

@app.route('/view', methods=['GET'])
def viewData():
    id = request.args.get('id')
    filename = os.path.join(app.static_folder, 'data', 'appointment.json')
    passData = {}
    
    
    
    with open(filename) as json_file: 
        data = json.load(json_file)

        for check in data['appointments']:
            print(check['id'])
            if(check['id'] == str(id)):
                passData['name'] = check['name']
                passData['comment'] = check['comment']
                passData['date'] = check['date']
                passData['time_in'] = check['time_in']
                passData['time_out'] = check['time_out']
                
                break
    if(passData == {}):
        return jsonify('Ttime errorors'), 400
        
    return jsonify(passData), 200


@app.route('/edit', methods=['POST'])
def editData():
    id = request.json['data']['id']
    print(id)
    filename = os.path.join(app.static_folder, 'data', 'appointment.json')
    
    with open(filename) as json_file: 
        data = json.load(json_file)
        add = request.json['data']
        
        for check in data['appointments']:
            if(check['id'] == str(id)):
                print('same')
                continue
            if(check['date']  == add['date']):
                print('enter')
                if(add['time_in'] <= check['time_out'] and add['time_in'] >= check['time_in']):
                    return jsonify('Ttime error'), 400
                if(add['time_out'] <= check['time_out'] and add['time_out'] >= check['time_in']):
                    return jsonify('Ttime errorors'), 400

        for check in data['appointments']:
            print(check['id'])
            if(check['id'] == str(id)):
                check['name'] = request.json['data']['name']
                check['comment'] = request.json['data']['comment']
                check['date'] = request.json['data']['date']
                check['time_in'] = request.json['data']['time_in']
                check['time_out'] = request.json['data']['time_out']
                break;
            
        print(data['appointments'])
        
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)
            
        
    return jsonify('Success'), 200

@app.route('/delete', methods=['POST'])
def delete():
    id = request.json['data']['id']
    filename = os.path.join(app.static_folder, 'data', 'appointment.json')
    
    with open(filename) as json_file: 
        data = json.load(json_file)
        for check in data['appointments']:
            
            if(check['id'] == str(id)):
                data['appointments'].remove(check)
                
                break
            
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)
    
    return jsonify('Success'), 200
        

if __name__ == '__main__':
    app.run(debug='true', host='127.0.0.1', port=5000)